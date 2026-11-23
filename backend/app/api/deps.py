from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import token_subject
from app.models import Merchant

bearer=HTTPBearer(auto_error=False)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def current_merchant(request:Request,auth:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db))->Merchant:
    token=auth.credentials if auth else request.cookies.get("udharpay_session")
    if not token: raise HTTPException(401,"Sign in to continue")
    mid=token_subject(token)
    merchant=db.get(Merchant,mid) if mid else None
    if not merchant: raise HTTPException(401,"Session expired")
    return merchant
