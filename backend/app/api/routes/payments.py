import uuid,base64,hmac,hashlib
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter,Depends,HTTPException,Request
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from app.api.deps import get_db,current_merchant
from app.models import Merchant,Customer,Payment,KhataTransaction,AuditLog
from app.core.config import settings
from app.services.cashfree_service import CashfreeService
router=APIRouter(prefix="/payments",tags=["Payments"])
class LinkIn(BaseModel): customer_id:int; amount:Decimal|None=None
@router.post("/create-demo-link")
def create_demo_link(body:LinkIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    amount=body.amount or c.outstanding_balance
    if amount<=0 or amount>c.outstanding_balance: raise HTTPException(422,"Demo request amount must be positive and cannot exceed the balance")
    order_id="demo_"+uuid.uuid4().hex
    p=Payment(merchant_id=m.id,customer_id=c.id,cashfree_order_id=order_id,amount=amount,payment_status="PENDING",payment_method="demo_link")
    db.add(p); db.add(AuditLog(merchant_id=m.id,action="demo_payment_link_created",entity_type="payment",entity_id=order_id)); db.commit()
    return {"id":p.id,"order_id":order_id,"amount":str(amount),"status":"PENDING","mode":"demo","share_url":settings.frontend_url.rstrip("/")+"/demo-pay/"+order_id,"customer_phone":c.phone,"customer_name":c.name,"shop_name":m.shop_name}
@router.post("/create-link")
async def create_link(body:LinkIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    c=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).first()
    if not c: raise HTTPException(404,"Customer not found")
    amount=body.amount or c.outstanding_balance
    if amount<=0 or amount>c.outstanding_balance: raise HTTPException(422,"Payment amount must be positive and cannot exceed the balance")
    order_id="udhar_"+uuid.uuid4().hex[:24]
    service=CashfreeService()
    try: result=await service.create_order(order_id,float(amount),str(c.id),c.phone or "")
    except Exception: raise HTTPException(502,"Cashfree could not create the order. Check integration settings and try again.")
    p=Payment(merchant_id=m.id,customer_id=c.id,cashfree_order_id=order_id,amount=amount,payment_status="PENDING",payment_method="cashfree_sandbox" if service.configured else "demo_pending")
    db.add(p); db.add(AuditLog(merchant_id=m.id,action="payment_order_created",entity_type="payment",entity_id=order_id)); db.commit()
    return {"id":p.id,"order_id":order_id,"amount":str(amount),"status":"PENDING","mode":"cashfree" if service.configured else "demo","environment":settings.cashfree_environment if service.configured else None,"payment_session_id":result.get("payment_session_id"),"checkout_url":result.get("payment_link")}
@router.get("/history")
def history(db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    rows=db.query(Payment,Customer.name).join(Customer,Customer.id==Payment.customer_id).filter(Payment.merchant_id==m.id).order_by(Payment.created_at.desc()).limit(100).all()
    return [{"id":p.id,"order_id":p.cashfree_order_id,"customer":n,"amount":str(p.amount),"status":p.payment_status,"method":p.payment_method,"created_at":p.created_at.isoformat()} for p,n in rows]
@router.get("/{payment_id}")
def get_payment(payment_id:int,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    p=db.query(Payment).filter_by(id=payment_id,merchant_id=m.id).first()
    if not p: raise HTTPException(404,"Payment not found")
    return {"id":p.id,"order_id":p.cashfree_order_id,"amount":str(p.amount),"status":p.payment_status}
webhook_router=APIRouter(prefix="/webhooks",tags=["Webhooks"])
@router.get("/demo-link/{order_id}")
def demo_link_info(order_id:str,db:Session=Depends(get_db)):
    row=db.query(Payment,Merchant.shop_name).join(Merchant,Merchant.id==Payment.merchant_id).filter(Payment.cashfree_order_id==order_id,Payment.payment_method=="demo_link").first()
    if not row: raise HTTPException(404,"Demo payment request not found")
    p,shop_name=row
    return {"order_id":p.cashfree_order_id,"amount":str(p.amount),"status":p.payment_status,"shop_name":shop_name,"created_at":p.created_at.isoformat(),"demo":True}
@webhook_router.post("/cashfree")
async def cashfree_webhook(request:Request,db:Session=Depends(get_db)):
    raw=await request.body(); signature=request.headers.get("x-webhook-signature"); timestamp=request.headers.get("x-webhook-timestamp")
    from app.core.config import settings
    if not settings.cashfree_client_secret or not signature or not timestamp: raise HTTPException(401,"Invalid webhook signature")
    expected=base64.b64encode(hmac.new(settings.cashfree_client_secret.encode(),timestamp.encode()+raw,hashlib.sha256).digest()).decode()
    if not hmac.compare_digest(expected,signature): raise HTTPException(401,"Invalid webhook signature")
    try:
        data=await request.json()
    except Exception:
        raise HTTPException(400,"Invalid webhook payload")
    # Cashfree's dashboard endpoint test can send a signed sample event without
    # an order object. Acknowledge it after signature verification, but never
    # mutate a payment unless the full order/payment payload is present.
    event_data=data.get("data") if isinstance(data,dict) else None
    if not isinstance(event_data,dict) or not isinstance(event_data.get("order"),dict):
        return {"ok":True,"ignored":"test_or_unrecognized_payload"}
    order=event_data["order"]
    payment_data=event_data.get("payment",{})
    if not isinstance(payment_data,dict):
        return {"ok":True,"ignored":"test_or_unrecognized_payload"}
    p=db.query(Payment).filter_by(cashfree_order_id=order.get("order_id")).with_for_update().first()
    if not p: return {"ok":True,"ignored":"unknown_order"}
    if p.payment_status=="SUCCESS": return {"ok":True,"duplicate":True}
    if data.get("type")=="PAYMENT_SUCCESS_WEBHOOK" and payment_data.get("payment_status")=="SUCCESS":
        if Decimal(str(order.get("order_amount")))!=p.amount: raise HTTPException(400,"Webhook amount does not match order")
        c=db.query(Customer).filter_by(id=p.customer_id,merchant_id=p.merchant_id).with_for_update().first()
        if not c: raise HTTPException(404,"Payment customer not found")
        if p.amount>c.outstanding_balance: raise HTTPException(409,"Payment exceeds current outstanding balance")
        p.payment_status="SUCCESS"; p.paid_at=datetime.utcnow(); c.outstanding_balance-=p.amount
        db.add(KhataTransaction(merchant_id=p.merchant_id,customer_id=c.id,transaction_type="PAYMENT",amount=p.amount,description="Verified Cashfree payment",status="verified")); db.commit()
    elif data.get("type")=="PAYMENT_FAILED_WEBHOOK": p.payment_status="FAILED"; db.commit()
    return {"ok":True}
