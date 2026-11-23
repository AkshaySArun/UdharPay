from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base,engine
from app.core.config import settings
from app import models
from app.services.demo_seed import seed_demo_data
from app.core.rate_limit import RateLimitMiddleware
from app.api.routes import auth,customers,khata,khata_import,dashboard,collections,payments,sarvam

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.demo_mode: seed_demo_data()
    yield
app=FastAPI(title="UdharPay AI API",version="1.0.0",description="Digital khata and respectful collections for small shops",lifespan=lifespan)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_url],allow_credentials=True,allow_methods=["GET","POST","PUT","DELETE","OPTIONS"],allow_headers=["Authorization","Content-Type"])
for route in (auth.router,customers.router,khata.router,khata_import.router,dashboard.router,collections.router,payments.router,payments.webhook_router,sarvam.router): app.include_router(route,prefix="/api")
@app.get("/api/health")
def health():
    sarvam_calls_configured=all((settings.sarvam_voice_api_key,settings.sarvam_voice_org_id,settings.sarvam_voice_workspace_id,settings.sarvam_voice_app_id,settings.sarvam_voice_connection_id,settings.sarvam_voice_agent_phone_number))
    return {"status":"ok","demo_mode":settings.demo_mode,"integrations":{"sarvam":"configured" if settings.sarvam_api_key else "demo","sarvam_voice_calls":"configured" if sarvam_calls_configured else "incomplete","cashfree":"configured" if settings.cashfree_client_id and settings.cashfree_client_secret else "demo"}}
