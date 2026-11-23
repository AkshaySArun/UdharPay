from datetime import date,datetime,timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Merchant,Customer,KhataTransaction,Payment

DEMO_PHONE="9999999999"
DEMO_PASSWORD="Demo@UdharPay2026"

def seed_demo_data():
    db:Session=SessionLocal()
    try:
        merchant=db.query(Merchant).filter_by(phone=DEMO_PHONE).first()
        if merchant: return
        merchant=Merchant(shop_name="Sharma General Store",owner_name="Ananya Sharma",phone=DEMO_PHONE,email="demo@udharpay.local",password_hash=hash_password(DEMO_PASSWORD),preferred_language="hi-IN")
        db.add(merchant); db.flush()
        data=[("Ramesh","9999900001","hi-IN","847",14),("Sunita","9999900002","hi-IN","1240",4),("Mahesh","9999900003","kn-IN","340",25),("Priya","9999900004","en-IN","2500",36),("Arun","9999900005","ta-IN","650",9)]
        people=[]
        for name,phone,language,balance,days in data:
            customer=Customer(merchant_id=merchant.id,name=name,phone=phone,preferred_language=language,outstanding_balance=Decimal(balance))
            db.add(customer); db.flush(); people.append(customer)
            opening_credit=Decimal(balance)+(Decimal("200") if name=="Ramesh" else Decimal("0"))
            db.add(KhataTransaction(merchant_id=merchant.id,customer_id=customer.id,transaction_type="CREDIT",amount=opening_credit,description="Monthly grocery purchases",transaction_date=date.today()-timedelta(days=days+4),due_date=date.today()-timedelta(days=days),status="recorded"))
        db.add(KhataTransaction(merchant_id=merchant.id,customer_id=people[0].id,transaction_type="PAYMENT",amount=Decimal("200"),description="Cash payment",transaction_date=date.today()-timedelta(days=2),status="recorded"))
        db.add(Payment(merchant_id=merchant.id,customer_id=people[1].id,cashfree_order_id="demo_pending_001",amount=Decimal("250"),payment_status="PENDING",payment_method="demo_pending"))
        db.add(Payment(merchant_id=merchant.id,customer_id=people[2].id,cashfree_order_id="demo_failed_001",amount=Decimal("100"),payment_status="FAILED",payment_method="demo_simulated"))
        db.commit()
    except Exception:
        db.rollback(); raise
    finally: db.close()
