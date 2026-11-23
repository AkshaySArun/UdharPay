from datetime import date
from decimal import Decimal
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from app.api.deps import get_db,current_merchant
from app.models import Customer,Merchant,KhataTransaction,AuditLog
from app.services.sarvam_service import SarvamService
router=APIRouter(prefix="/khata",tags=["Digital Khata"])
class TxIn(BaseModel): customer_id:int; transaction_type:str; amount:Decimal=Field(gt=0,le=10000000); description:str=""; transaction_date:date|None=None; due_date:date|None=None
class ImportRow(BaseModel): name:str=Field(min_length=2,max_length=120); phone:str|None=None; amount:Decimal=Field(gt=0,le=10000000); transaction_date:date|None=None; description:str=""; preferred_language:str="hi-IN"
class ApproveImport(BaseModel): entries:list[ImportRow]
class VoiceEntry(BaseModel): transcript:str=Field(min_length=3,max_length=2500); language_code:str="hi-IN"
@router.get("")
def ledger(db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    rows=db.query(KhataTransaction,Customer.name).join(Customer,Customer.id==KhataTransaction.customer_id).filter(KhataTransaction.merchant_id==m.id).order_by(KhataTransaction.transaction_date.desc(),KhataTransaction.id.desc()).limit(200).all()
    return [{"id":t.id,"customer_id":t.customer_id,"customer_name":name,"type":t.transaction_type,"amount":str(t.amount),"description":t.description,"date":t.transaction_date.isoformat(),"due_date":t.due_date.isoformat() if t.due_date else None,"status":t.status} for t,name in rows]
@router.post("/transactions")
def create(body:TxIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    if body.transaction_type not in ("CREDIT","PAYMENT","ADJUSTMENT"): raise HTTPException(422,"Invalid transaction type")
    c=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).with_for_update().first()
    if not c: raise HTTPException(404,"Customer not found")
    delta=body.amount if body.transaction_type=="CREDIT" else -body.amount
    if body.transaction_type=="PAYMENT" and body.amount>c.outstanding_balance: raise HTTPException(422,"Payment cannot exceed the outstanding balance")
    c.outstanding_balance=max(Decimal("0.00"),c.outstanding_balance+delta)
    t=KhataTransaction(merchant_id=m.id,transaction_date=body.transaction_date or date.today(),status="recorded",**body.model_dump(exclude={"transaction_date"}))
    db.add(t); db.add(AuditLog(merchant_id=m.id,action="ledger_entry_created",entity_type="transaction",entity_id="pending")); db.commit(); db.refresh(t)
    return {"id":t.id,"customer_id":t.customer_id,"type":t.transaction_type,"amount":str(t.amount),"balance":str(c.outstanding_balance),"status":t.status}
@router.post("/approve-import")
def approve_import(body:ApproveImport,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    if not body.entries or len(body.entries)>100: raise HTTPException(422,"Provide between 1 and 100 reviewed entries")
    saved=[]
    for row in body.entries:
        c=db.query(Customer).filter_by(merchant_id=m.id,phone=row.phone).first() if row.phone else None
        if c is None: c=Customer(merchant_id=m.id,name=row.name,phone=row.phone,preferred_language=row.preferred_language); db.add(c); db.flush()
        c.outstanding_balance+=row.amount
        t=KhataTransaction(merchant_id=m.id,customer_id=c.id,transaction_type="CREDIT",amount=row.amount,description=row.description or "Imported from khata",transaction_date=row.transaction_date or date.today(),status="recorded")
        db.add(t); saved.append(t)
    db.add(AuditLog(merchant_id=m.id,action="khata_import_approved",entity_type="transaction",entity_id=str(len(saved))))
    db.commit(); return {"approved":len(saved),"transaction_ids":[t.id for t in saved]}
@router.post("/voice-entry")
async def voice_entry(body:VoiceEntry,m:Merchant=Depends(current_merchant)):
    service=SarvamService()
    try:
        result=await service.chat([{"role":"system","content":f"The source language is {body.language_code}. Extract one proposed kirana credit ledger entry. Return only JSON: {{name:string, phone:string|null, amount:number|null, date:string|null, description:string, confidence:number}}. Never guess missing information. This proposal requires merchant approval."},{"role":"user","content":body.transcript}])
        import json
        return {"proposal":json.loads(result["choices"][0]["message"]["content"]),"requires_merchant_approval":True,"saved":False}
    except RuntimeError as e: raise HTTPException(503,str(e))
    except Exception: raise HTTPException(502,"Voice entry extraction failed")
