from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db,current_merchant
from app.models import Merchant,Customer,KhataTransaction,CollectionTask,Conversation
from app.agents.decision_engine import priority
from app.agents.conversation_agent import classify
router=APIRouter(prefix="/collections",tags=["AI Collections"])
@router.get("/tasks")
def tasks(db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    people=db.query(Customer).filter(Customer.merchant_id==m.id,Customer.outstanding_balance>0,Customer.collection_opt_out.is_(False)).all(); out=[]
    for c in people:
        due=db.query(KhataTransaction.due_date).filter_by(merchant_id=m.id,customer_id=c.id,transaction_type="CREDIT").order_by(KhataTransaction.due_date.desc()).first()
        score,reason=priority(c.outstanding_balance,due[0] if due else None)
        task=db.query(CollectionTask).filter_by(merchant_id=m.id,customer_id=c.id).order_by(CollectionTask.id.desc()).first()
        out.append({"customer_id":c.id,"customer_name":c.name,"phone":c.phone,"balance":str(c.outstanding_balance),"priority":score,"reason":reason,"status":task.status if task else "queued","language":c.preferred_language})
    return sorted(out,key=lambda x:x["priority"],reverse=True)
class TaskAction(BaseModel): customer_id:int
@router.post("/start")
def start(body:TaskAction,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).first()
    if not c or c.outstanding_balance<=0: raise HTTPException(404,"Customer with an outstanding balance not found")
    if c.collection_opt_out: raise HTTPException(409,"This customer has opted out of collection follow-ups")
    task=CollectionTask(merchant_id=m.id,customer_id=c.id,status="active",priority=priority(c.outstanding_balance,None)[0]); db.add(task)
    greeting=f"Namaste {c.name} ji. {m.shop_name} mein aapka ₹{c.outstanding_balance:.2f} balance baaki hai. Kya aap payment karna chahenge?"
    db.add(Conversation(merchant_id=m.id,customer_id=c.id,language=c.preferred_language,message=greeting,sender="agent",intent="COLLECTION_START")); db.commit()
    return {"status":"active","mode":"simulator","message":greeting,"customer_id":c.id}
@router.post("/pause")
def pause(body:TaskAction,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    t=db.query(CollectionTask).filter_by(merchant_id=m.id,customer_id=body.customer_id,status="active").first()
    if not t: raise HTTPException(404,"No active task")
    t.status="paused"; db.commit(); return {"status":"paused"}
@router.post("/stop")
def stop(body:TaskAction,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    t=db.query(CollectionTask).filter_by(merchant_id=m.id,customer_id=body.customer_id,status="active").first()
    if not t: raise HTTPException(404,"No active task")
    t.status="stopped"; t.completed_at=datetime.utcnow(); db.commit(); return {"status":"stopped"}
class ResponseIn(BaseModel): customer_id:int; message:str; language:str="hi-IN"
@router.post("/customer-response")
def response(body:ResponseIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    intent=classify(body.message)
    if intent=="OPT_OUT":
        c.collection_opt_out=True
        for task in db.query(CollectionTask).filter_by(merchant_id=m.id,customer_id=c.id).filter(CollectionTask.status.in_(["active","queued"])).all(): task.status="stopped"; task.completed_at=datetime.utcnow()
    db.add(Conversation(merchant_id=m.id,customer_id=c.id,language=body.language,message=body.message,sender="customer",intent=intent)); db.commit()
    replies={"REQUEST_PAYMENT_LINK":"Certainly. I can prepare a secure payment link for you.","PAY_LATER":"Understood. We’ll make a note and follow up later.","ALREADY_PAID":"Thanks for letting us know. Please share the payment reference so we can verify it.","DISPUTE_AMOUNT":"Thanks for flagging this. We’ve paused follow ups while the shop reviews your account.","REQUEST_HUMAN_HELP":"We’ve noted this. Someone from the shop can help you shortly.","OPT_OUT":"Understood. We’ll stop collection messages.","PAY_PARTIALLY":"You can choose an amount up to your outstanding balance when requesting a payment link."}
    return {"intent":intent,"reply":replies[intent],"payment_link_available":intent=="REQUEST_PAYMENT_LINK"}
