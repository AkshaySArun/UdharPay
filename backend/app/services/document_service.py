import asyncio, tempfile, os, zipfile, io
from pathlib import Path
from sarvamai import SarvamAI
from app.core.config import settings

def _parse_document(name:str,content:bytes,content_type:str,language:str):
    client=SarvamAI(api_subscription_key=settings.sarvam_api_key)
    suffix=os.path.splitext(name)[1] or (".pdf" if "pdf" in content_type else ".jpg")
    with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as f:
        f.write(content); temp_path=f.name
    try:
        with open(temp_path,"rb") as source:
            job=client.doc_ai.parse(file=[(name,source,content_type)],language=language,content_type="handwritten")
        terminal={"completed","partially_completed","failed","rejected"}
        for _ in range(60):
            status=client.doc_ai.get_status(job_id=job.job_id)
            state=status.status.lower()
            if state in terminal: break
            import time; time.sleep(2)
        if state not in {"completed","partially_completed"}: raise RuntimeError("Sarvam document processing did not complete")
        download=client.doc_ai.get_download_url(job_id=job.job_id)
        import httpx
        response=httpx.get(download.url,timeout=30); response.raise_for_status()
        archive=zipfile.ZipFile(io.BytesIO(response.content))
        return "\n".join(archive.read(n).decode("utf-8","replace") for n in archive.namelist() if n.lower().endswith((".md",".txt",".html",".json")))[:30000]
    finally:
        Path(temp_path).unlink(missing_ok=True)

async def parse_document(name:str,content:bytes,content_type:str,language:str):
    return await asyncio.to_thread(_parse_document,name,content,content_type,language)
