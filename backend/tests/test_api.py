from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base
from app.api.deps import get_db
from app.agents.conversation_agent import classify
from app.agents.decision_engine import priority

@pytest.fixture
def client():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
    def override_db():
        db=Session()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override_db
    with TestClient(app) as test:
        yield test
    app.dependency_overrides.clear(); engine.dispose()

def register(client,phone):
    response=client.post("/api/auth/register",json={"shop_name":"Sharma Store","owner_name":"Meera","phone":phone,"email":None,"password":"strong-password-1"})
    assert response.status_code==200,response.text

def test_register_cookie_and_merchant_isolation(client):
    register(client,"9100000001")
    customer=client.post("/api/customers",json={"name":"Ramesh","phone":"9100000002"}).json()
    register(client,"9100000003")
    assert client.get(f"/api/customers/{customer['id']}").status_code==404

def test_credit_updates_balance_and_prevents_overpayment(client):
    register(client,"9100000011")
    cid=client.post("/api/customers",json={"name":"Sunita"}).json()["id"]
    credit=client.post("/api/khata/transactions",json={"customer_id":cid,"transaction_type":"CREDIT","amount":"1200"})
    assert credit.status_code==200 and credit.json()["balance"]=="1200.00"
    payment=client.post("/api/khata/transactions",json={"customer_id":cid,"transaction_type":"PAYMENT","amount":"1201"})
    assert payment.status_code==422
    assert client.get("/api/customers").json()[0]["outstanding_balance"]=="1200.00"

def test_opt_out_removes_customer_from_collection_queue(client):
    register(client,"9100000021")
    cid=client.post("/api/customers",json={"name":"Arun"}).json()["id"]
    client.post("/api/khata/transactions",json={"customer_id":cid,"transaction_type":"CREDIT","amount":"500"})
    assert client.post("/api/collections/customer-response",json={"customer_id":cid,"message":"stop messaging"}).json()["intent"]=="OPT_OUT"
    assert client.get("/api/collections/tasks").json()==[]
    assert client.post("/api/collections/start",json={"customer_id":cid}).status_code==409

def test_agent_intent_and_explainable_priority():
    assert classify("please send me a payment link")=="REQUEST_PAYMENT_LINK"
    assert classify("stop messaging me")=="OPT_OUT"
    score,reason=priority(Decimal("1000"),None)
    assert score==20 and "outstanding" in reason
