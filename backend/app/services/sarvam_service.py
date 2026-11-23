import httpx
from app.core.config import settings

class SarvamVoiceAgentService:
    @property
    def configured(self):
        return bool(settings.sarvam_voice_api_key and settings.sarvam_voice_org_id and settings.sarvam_voice_workspace_id and settings.sarvam_voice_app_id and settings.sarvam_voice_connection_id and settings.sarvam_voice_agent_phone_number)

    async def start_outbound_call(self, customer_name:str, shop_name:str, amount:str, language_code:str, due_date:str=""):
        if not self.configured:
            raise RuntimeError("Sarvam Voice Agent is not fully configured. Add its Voice Agents API key, org, workspace, app, connection, and caller number settings to backend/.env.")
        languages={"hi-IN":"Hindi","en-IN":"English","kn-IN":"Kannada","ta-IN":"Tamil","te-IN":"Telugu","mr-IN":"Marathi"}
        greeting_templates={
            "hi-IN":f"नमस्ते {customer_name} जी। मैं {shop_name} से बोल रहा हूँ। क्या अभी बात करने का सही समय है?",
            "en-IN":f"Hello, may I speak with {customer_name}? I am calling from {shop_name} with a quick account reminder. Is now a good time?",
            "kn-IN":f"ನಮಸ್ಕಾರ {customer_name} ಅವರೇ. ನಾನು {shop_name} ನಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇನೆ. ಈಗ ಮಾತನಾಡಲು ಅನುಕೂಲವೇ?",
            "ta-IN":f"வணக்கம் {customer_name}. நான் {shop_name} கடையிலிருந்து பேசுகிறேன். இப்போது பேசலாமா?",
            "te-IN":f"నమస్కారం {customer_name}. నేను {shop_name} నుండి మాట్లాడుతున్నాను. ఇప్పుడు మాట్లాడటం సౌకర్యంగా ఉందా?",
            "mr-IN":f"नमस्कार {customer_name}. मी {shop_name} मधून बोलत आहे. आत्ता बोलणे सोयीचे आहे का?",
        }
        greeting=greeting_templates.get(language_code,greeting_templates["hi-IN"])
        url=f"https://apps.sarvam.ai/api/outbounds/v1/orgs/{settings.sarvam_voice_org_id}/workspaces/{settings.sarvam_voice_workspace_id}/outbounds"
        payload={
            "app_config":{
                "app_id":settings.sarvam_voice_app_id,
                "app_version":settings.sarvam_voice_app_version,
                "connection_config":{"connection_id":settings.sarvam_voice_connection_id,"agent_phone_number":settings.sarvam_voice_agent_phone_number},
                "agent_variables":{"call_summary":"","commitment_date":"","disposition":"","due_date":due_date,"outstanding_amount":amount,"payment_link_sent":"false","payment_status":"pending","user_name":customer_name},
                "app_overrides":{"initial_bot_message":greeting,"initial_language_name":languages.get(language_code,"Hindi")},
            },
            "user_config":{"user_phone_number":settings.sarvam_voice_test_phone_number},
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response=await client.post(url,json=payload,headers={"X-API-Key":settings.sarvam_voice_api_key,"Content-Type":"application/json"})
            response.raise_for_status()
            return response.json()

class SarvamService:
    @property
    def configured(self): return bool(settings.sarvam_api_key)
    async def chat(self, messages):
        if not self.configured: raise RuntimeError("Sarvam is not configured. Add SARVAM_API_KEY to backend/.env.")
        async with httpx.AsyncClient(timeout=45) as client:
            r=await client.post(settings.sarvam_base_url.rstrip("/")+"/v1/chat/completions",headers={"api-subscription-key":settings.sarvam_api_key},json={"model":"sarvam-105b","messages":messages,"temperature":0.1,"reasoning_effort":None,"response_format":{"type":"json_object"}})
            r.raise_for_status(); return r.json()
    async def transcribe(self, file, language_code:str|None=None):
        if not self.configured: raise RuntimeError("Sarvam is not configured. Add SARVAM_API_KEY to backend/.env.")
        data={"model":"saaras:v4","mode":"transcribe"}
        if language_code: data["language_code"]=language_code
        async with httpx.AsyncClient(timeout=60) as client:
            r=await client.post(settings.sarvam_base_url.rstrip("/")+"/speech-to-text",headers={"api-subscription-key":settings.sarvam_api_key},data=data,files={"file":file})
            r.raise_for_status(); return r.json()
    async def synthesize(self,text:str,language_code:str):
        if not self.configured: raise RuntimeError("Sarvam is not configured. Add SARVAM_API_KEY to backend/.env.")
        speakers={"hi-IN":"priya","en-IN":"ishita","te-IN":"priya","kn-IN":"ishita","ta-IN":"ishita","mr-IN":"priya"}
        async with httpx.AsyncClient(timeout=45) as client:
            r=await client.post(settings.sarvam_base_url.rstrip("/")+"/text-to-speech",headers={"api-subscription-key":settings.sarvam_api_key},json={"text":text,"language_code":language_code,"model":"bulbul:v3","speaker":speakers.get(language_code,"priya"),"output_audio_codec":"mp3"})
            r.raise_for_status(); return r.json()
