from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db,current_merchant
from app.models import Customer,Merchant,KhataTransaction
router=APIRouter(prefix="/customers",tags=["Customers"])
class CustomerIn(BaseModel): name:str=Field(min_length=2,max_length=120); phone:str|None=None; preferred_language:str="hi-IN"
def item(c,db):
    last=db.query(func.max(KhataTransaction.transaction_date)).filter_by(customer_id=c.id,merchant_id=c.merchant_id).scalar()
    return {"id":c.id,"name":c.name,"phone":c.phone,"preferred_language":c.preferred_language,"outstanding_balance":str(c.outstanding_balance),"collection_opt_out":c.collection_opt_out,"created_at":c.created_at.isoformat(),"last_transaction":last.isoformat() if last else None}
@router.get("")
def list_customers(q:str="",db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    query=db.query(Customer).filter(Customer.merchant_id==m.id)
    if q: query=query.filter(Customer.name.ilike(f"%{q}%"))
    return [item(c,db) for c in query.order_by(Customer.name).all()]
@router.post("")
def create(body:CustomerIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    if body.phone and db.query(Customer).filter_by(merchant_id=m.id,phone=body.phone).first(): raise HTTPException(409,"This phone number is already in your customers")
    c=Customer(merchant_id=m.id,**body.model_dump()); db.add(c); db.commit(); db.refresh(c); return item(c,db)
@router.get("/{customer_id}")
def detail(customer_id:int,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    return {**item(c,db),"transactions":[{"id":t.id,"type":t.transaction_type,"amount":str(t.amount),"description":t.description,"date":t.transaction_date.isoformat(),"status":t.status} for t in db.query(KhataTransaction).filter_by(customer_id=c.id,merchant_id=m.id).order_by(KhataTransaction.transaction_date.desc()).all()]}
@router.put("/{customer_id}")
def update(customer_id:int,body:CustomerIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    for k,v in body.model_dump().items(): setattr(c,k,v)
    db.commit(); db.refresh(c); return item(c,db)
@router.delete("/{customer_id}")
def delete(customer_id:int,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    db.delete(c); db.commit(); return {"ok":True}
