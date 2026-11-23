from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, Numeric, Index, UniqueConstraint, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Merchant(Base):
    __tablename__="merchants"
    id: Mapped[int]=mapped_column(primary_key=True)
    shop_name: Mapped[str]=mapped_column(String(120))
    owner_name: Mapped[str]=mapped_column(String(120))
    phone: Mapped[str]=mapped_column(String(20), unique=True, index=True)
    email: Mapped[str|None]=mapped_column(String(255), unique=True, nullable=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    preferred_language: Mapped[str]=mapped_column(String(24), default="hi-IN")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__="customers"
    __table_args__=(UniqueConstraint("merchant_id","phone",name="uq_customer_merchant_phone"), Index("ix_customers_merchant_name","merchant_id","name"))
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    name: Mapped[str]=mapped_column(String(120))
    phone: Mapped[str|None]=mapped_column(String(20),nullable=True)
    preferred_language: Mapped[str]=mapped_column(String(24),default="hi-IN")
    outstanding_balance: Mapped[Decimal]=mapped_column(Numeric(12,2),default=Decimal("0"))
    collection_opt_out: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class KhataTransaction(Base):
    __tablename__="khata_transactions"
    __table_args__=(Index("ix_ledger_merchant_date","merchant_id","transaction_date"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id",ondelete="CASCADE"),index=True)
    transaction_type: Mapped[str]=mapped_column(String(16))
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    description: Mapped[str]=mapped_column(String(255),default="")
    transaction_date: Mapped[date]=mapped_column(Date,default=date.today)
    due_date: Mapped[date|None]=mapped_column(Date,nullable=True)
    status: Mapped[str]=mapped_column(String(24),default="recorded")
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class Payment(Base):
    __tablename__="payments"
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id",ondelete="CASCADE"),index=True)
    cashfree_order_id: Mapped[str]=mapped_column(String(64),unique=True,index=True)
    payment_link_id: Mapped[str|None]=mapped_column(String(128),nullable=True)
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    payment_status: Mapped[str]=mapped_column(String(24),default="PENDING")
    payment_method: Mapped[str]=mapped_column(String(32),default="cashfree")
    paid_at: Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class CollectionTask(Base):
    __tablename__="collection_tasks"
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id",ondelete="CASCADE"),index=True)
    priority: Mapped[int]=mapped_column(Integer,default=0)
    status: Mapped[str]=mapped_column(String(24),default="queued")
    scheduled_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    completed_at: Mapped[datetime|None]=mapped_column(DateTime,nullable=True)

class Conversation(Base):
    __tablename__="conversations"
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id",ondelete="CASCADE"),index=True)
    language: Mapped[str]=mapped_column(String(24),default="hi-IN")
    message: Mapped[str]=mapped_column(Text)
    sender: Mapped[str]=mapped_column(String(16))
    intent: Mapped[str]=mapped_column(String(32),default="UNKNOWN")
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class AuditLog(Base):
    __tablename__="audit_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    merchant_id: Mapped[int]=mapped_column(ForeignKey("merchants.id",ondelete="CASCADE"),index=True)
    action: Mapped[str]=mapped_column(String(80))
    entity_type: Mapped[str]=mapped_column(String(40))
    entity_id: Mapped[str]=mapped_column(String(64))
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
