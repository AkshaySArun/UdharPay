from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
pwd = CryptContext(schemes=["argon2"], deprecated="auto")
ALGORITHM="HS256"
def hash_password(value:str)->str: return pwd.hash(value)
def verify_password(value:str, hashed:str)->bool: return pwd.verify(value,hashed)
def create_token(merchant_id:int)->str:
    return jwt.encode({"sub":str(merchant_id),"exp":datetime.now(timezone.utc)+timedelta(hours=24)},settings.jwt_secret_key,algorithm=ALGORITHM)
def token_subject(token:str)->int|None:
    try: return int(jwt.decode(token,settings.jwt_secret_key,algorithms=[ALGORITHM])["sub"])
    except (JWTError,ValueError,KeyError): return None
