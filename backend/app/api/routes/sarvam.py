import json
import httpx
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form
from pydantic import BaseModel
from app.api.deps import current_merchant
from app.models import Merchant,Customer,AuditLog,KhataTransaction
from app.services.sarvam_service import SarvamService,SarvamVoiceAgentService
from app.api.deps import get_db
from app.core.config import settings
from sqlalchemy.orm import Session
router=APIRouter(prefix="/sarvam",tags=["Sarvam AI"])
class TextIn(BaseModel): text:str; language_code:str="hi-IN"
class OutboundCallIn(BaseModel): customer_id:int
@router.post("/outbound-call")
async def outbound_call(body:OutboundCallIn,db:Session=Depends(get_db),m:Merchant=Depends(current_merchant)):
    customer=db.query(Customer).filter_by(id=body.customer_id,merchant_id=m.id).first()
    if not customer: raise HTTPException(404,"Customer not found")
    if customer.collection_opt_out: raise HTTPException(409,"This customer has opted out of collection calls")
    if customer.outstanding_balance<=0: raise HTTPException(409,"This customer has no outstanding balance")
    due_row=db.query(KhataTransaction.due_date).filter_by(merchant_id=m.id,customer_id=customer.id,transaction_type="CREDIT").order_by(KhataTransaction.transaction_date.desc()).first()
    due_date=due_row[0].isoformat() if due_row and due_row[0] else ""
    service=SarvamVoiceAgentService()
    try:
        result=await service.start_outbound_call(customer.name,m.shop_name,str(customer.outstanding_balance),customer.preferred_language,due_date)
    except RuntimeError as e: raise HTTPException(503,str(e))
    except httpx.HTTPStatusError as e:
        status=e.response.status_code
        hint="Set SARVAM_VOICE_API_KEY from Voice Agents > Settings > API Key, and confirm it belongs to the configured workspace." if status in (401,403) else "Check Voice Agent billing or call credits." if status==402 else "Check that the configured app, version, connection, and phone numbers are valid." if status in (400,422) else "Check rate limits and try again." if status==429 else "Try again later."
        raise HTTPException(status if status in (402,429) else 502,f"Sarvam could not start the outbound call (HTTP {status}). {hint}") from None
    except httpx.TimeoutException: raise HTTPException(504,"Sarvam call request timed out. Check the Voice Agents call log before retrying.")
    except httpx.RequestError: raise HTTPException(502,"Could not reach Sarvam Voice Agents.")
    attempt_id=result.get("attempt_id") if isinstance(result,dict) else None
    if not attempt_id: raise HTTPException(502,"Sarvam accepted no call attempt. Check the Voice Agents call log.")
    db.add(AuditLog(merchant_id=m.id,action="sarvam_outbound_call_started",entity_type="customer",entity_id=str(customer.id)))
    db.commit()
    return {"status":"started","attempt_id":attempt_id,"customer_name":customer.name,"target_phone":settings.sarvam_voice_test_phone_number,"mode":"live"}
@router.post("/synthesize")
async def synthesize(body:TextIn,m:Merchant=Depends(current_merchant)):
    if not body.text or len(body.text)>2500: raise HTTPException(422,"Speech text must be between 1 and 2,500 characters")
    service=SarvamService()
    try:
        result=await service.synthesize(body.text,body.language_code)
        return {"audio_base64":result["audios"][0],"mime_type":"audio/mpeg","language_code":body.language_code}
    except RuntimeError as e: raise HTTPException(503,str(e))
    except Exception: raise HTTPException(502,"Sarvam speech synthesis failed")
@router.post("/transcribe")
async def transcribe(audio:UploadFile=File(...),language_code:str=Form("hi-IN"),m:Merchant=Depends(current_merchant)):
    if audio.size and audio.size>10*1024*1024: raise HTTPException(413,"Audio file exceeds 10 MB")
    if language_code not in {"hi-IN","en-IN","kn-IN","ta-IN","te-IN","mr-IN"}: raise HTTPException(422,"Unsupported voice language")
    service=SarvamService()
    try:
        content_type=(audio.content_type or "audio/webm").split(";",1)[0].strip()
        data=await service.transcribe((audio.filename,await audio.read(),content_type),language_code); return data
    except RuntimeError as e: raise HTTPException(503,str(e))
    except httpx.HTTPStatusError as e:
        status=e.response.status_code
        hint="Check the API key and model access." if status in (401,403) else "Check your Sarvam account billing, plan, or available credits." if status==402 else "Check Sarvam rate limits and try again shortly." if status==429 else "Check the audio format and try again." if status==400 else "Try again later."
        raise HTTPException(status if status in (401,402,403,429) else 502,f"Sarvam speech-to-text returned HTTP {status}. {hint}") from None
    except httpx.TimeoutException: raise HTTPException(504,"Sarvam speech-to-text timed out. Please retry.")
    except httpx.RequestError: raise HTTPException(502,"Could not reach Sarvam. Check the backend network and SARVAM_BASE_URL.")
@router.post("/extract")
async def extract(body:TextIn,m:Merchant=Depends(current_merchant)):
    service=SarvamService()
    try:
        result=await service.chat([{"role":"system","content":f"The source language is {body.language_code}. Extract a proposed Indian kirana credit entry from the text. Return only JSON: {{customer_name:string, phone:string|null, amount:number|null, date:string|null, description:string, confidence:number}}. Never guess missing fields; use null and low confidence."},{"role":"user","content":body.text}])
        raw=result["choices"][0]["message"]["content"]
        if not isinstance(raw,str) or not raw.strip(): raise ValueError("empty completion")
        proposal=json.loads(raw)
        if not isinstance(proposal,dict): raise ValueError("completion was not a JSON object")
        return {"proposal":proposal,"requires_merchant_approval":True}
    except RuntimeError as e: raise HTTPException(503,str(e))
    except httpx.HTTPStatusError as e:
        status=e.response.status_code
        hint="Check the API key and model access." if status in (401,403) else "Check your Sarvam account billing, plan, or available credits." if status==402 else "Check Sarvam rate limits and try again shortly." if status==429 else "Try again later."
        raise HTTPException(status if status in (401,402,403,429) else 502,f"Sarvam returned HTTP {status}. {hint}") from None
    except httpx.TimeoutException: raise HTTPException(504,"Sarvam took too long to respond. Please retry.")
    except (json.JSONDecodeError,KeyError,TypeError,ValueError): raise HTTPException(502,"Sarvam responded, but its result could not be read as a JSON proposal. Please retry.")
    except httpx.RequestError: raise HTTPException(502,"Could not reach Sarvam. Check the backend network and SARVAM_BASE_URL.")
