from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.api.deps import get_db, current_merchant
from app.core.security import hash_password, verify_password, create_token
from app.core.config import settings
from app.models import Merchant

router=APIRouter(prefix="/auth",tags=["Authentication"])
class Register(BaseModel): shop_name:str=Field(min_length=2,max_length=120); owner_name:str=Field(min_length=2,max_length=120); phone:str=Field(min_length=10,max_length=15); email:EmailStr|None=None; password:str=Field(min_length=8); preferred_language:str="hi-IN"
class Login(BaseModel): phone:str; password:str
def serialize(m): return {"id":m.id,"shop_name":m.shop_name,"owner_name":m.owner_name,"phone":m.phone,"email":m.email,"preferred_language":m.preferred_language}
def set_session(response:Response,merchant_id:int):
    response.set_cookie("udharpay_session",create_token(merchant_id),httponly=True,secure=settings.frontend_url.startswith("https://"),samesite="lax",max_age=86400,path="/")
@router.post("/register")
def register(body:Register,response:Response,db:Session=Depends(get_db)):
    if db.query(Merchant).filter((Merchant.phone==body.phone)|(Merchant.email==body.email if body.email else False)).first(): raise HTTPException(409,"A merchant with this phone or email already exists")
    m=Merchant(**body.model_dump(exclude={"password"}),password_hash=hash_password(body.password)); db.add(m); db.commit(); db.refresh(m)
    set_session(response,m.id); return {"merchant":serialize(m)}
@router.post("/login")
def login(body:Login,response:Response,db:Session=Depends(get_db)):
    m=db.query(Merchant).filter(Merchant.phone==body.phone).first()
    if not m or not verify_password(body.password,m.password_hash): raise HTTPException(401,"Phone number or password is incorrect")
    set_session(response,m.id); return {"merchant":serialize(m)}
@router.post("/demo")
def demo_login(response:Response,db:Session=Depends(get_db)):
    if not settings.demo_mode: raise HTTPException(404,"Demo mode is disabled")
    from app.services.demo_seed import DEMO_PHONE
    m=db.query(Merchant).filter_by(phone=DEMO_PHONE).first()
    if not m: raise HTTPException(503,"Demo account is not available yet")
    set_session(response,m.id); return {"merchant":serialize(m)}
@router.post("/logout")
def logout(response:Response):
    response.delete_cookie("udharpay_session",path="/",httponly=True,samesite="lax"); return {"ok":True}
@router.get("/me")
def me(m:Merchant=Depends(current_merchant)): return serialize(m)
