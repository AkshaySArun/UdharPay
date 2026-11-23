from datetime import date
from decimal import Decimal
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db,current_merchant
from app.models import Merchant,Customer,KhataTransaction
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    customers=db.query(Customer).filter_by(merchant_id=m.id).all()
    outstanding=sum((c.outstanding_balance for c in customers),Decimal("0"))
    overdue=db.query(func.count(func.distinct(KhataTransaction.customer_id))).filter(KhataTransaction.merchant_id==m.id,KhataTransaction.transaction_type=="CREDIT",KhataTransaction.due_date<date.today()).scalar() or 0
    start=date.today().replace(day=1)
    collected=db.query(func.coalesce(func.sum(KhataTransaction.amount),0)).filter(KhataTransaction.merchant_id==m.id,KhataTransaction.transaction_type=="PAYMENT",KhataTransaction.transaction_date>=start).scalar()
    txs=db.query(KhataTransaction,Customer.name).join(Customer,Customer.id==KhataTransaction.customer_id).filter(KhataTransaction.merchant_id==m.id).order_by(KhataTransaction.created_at.desc()).limit(7).all()
    top=sorted(customers,key=lambda c:c.outstanding_balance,reverse=True)[:5]
    return {"shop_name":m.shop_name,"total_outstanding":str(outstanding),"collected_this_month":str(collected),"customer_count":len(customers),"overdue_accounts":overdue,"collection_success_rate":round(float(collected)/(float(collected)+float(outstanding))*100) if float(collected)+float(outstanding)>0 else 0,"recent_transactions":[{"id":t.id,"customer":n,"type":t.transaction_type,"amount":str(t.amount),"date":t.transaction_date.isoformat(),"status":t.status} for t,n in txs],"top_customers":[{"id":c.id,"name":c.name,"balance":str(c.outstanding_balance)} for c in top],"demo_mode":True}
@router.get("/analytics")
def analytics(db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    result=[]
    for month in range(1,13):
        collected=db.query(func.coalesce(func.sum(KhataTransaction.amount),0)).filter(KhataTransaction.merchant_id==m.id,KhataTransaction.transaction_type=="PAYMENT",func.strftime("%Y-%m",KhataTransaction.transaction_date)==f"{date.today().year}-{month:02d}").scalar()
        result.append({"month":date(date.today().year,month,1).strftime("%b"),"collected":str(collected)})
    return result
