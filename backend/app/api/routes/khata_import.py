import json
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from app.api.deps import current_merchant
from app.models import Merchant
from app.core.config import settings
from app.services.document_service import parse_document
from app.services.sarvam_service import SarvamService

router=APIRouter(prefix="/khata",tags=["Digital Khata import"])
@router.post("/upload")
async def upload(file:UploadFile=File(...),m:Merchant=Depends(current_merchant)):
    content_type=file.content_type or ""
    if content_type not in ("image/jpeg","image/png","application/pdf"): raise HTTPException(415,"Upload a JPG, PNG, or PDF file")
    data=await file.read(settings.max_upload_size_mb*1024*1024+1)
    if len(data)>settings.max_upload_size_mb*1024*1024: raise HTTPException(413,"File exceeds the configured upload limit")
    if not settings.sarvam_api_key: raise HTTPException(503,"Sarvam is not configured. Add SARVAM_API_KEY to backend/.env.")
    try:
        text=await parse_document(file.filename or "khata.jpg",data,content_type,m.preferred_language)
        if not text.strip(): raise RuntimeError("No readable text was found")
        service=SarvamService()
        result=await service.chat([{"role":"system","content":"Extract handwritten kirana khata entries from the OCR text. Return only JSON with key customers containing an array of objects: name, phone (string or null), amount (number or null), date (YYYY-MM-DD or null), description, confidence (0 to 1). Never invent missing values. These are proposed records for merchant review."},{"role":"user","content":text}])
        proposal=json.loads(result["choices"][0]["message"]["content"])
        return {"source_text":text,"proposal":proposal,"requires_merchant_approval":True,"saved":False}
    except HTTPException: raise
    except Exception: raise HTTPException(502,"Document extraction failed. Review the image and try again.")
