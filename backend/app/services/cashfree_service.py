import httpx
from app.core.config import settings

class CashfreeService:
    @property
    def configured(self): return bool(settings.cashfree_client_id and settings.cashfree_client_secret)
    async def create_order(self, order_id:str, amount:float, customer_id:str, phone:str):
        if not self.configured: return {"mode":"demo","payment_session_id":None,"checkout_url":None}
        base="https://sandbox.cashfree.com/pg" if settings.cashfree_environment=="sandbox" else "https://api.cashfree.com/pg"
        headers={"x-client-id":settings.cashfree_client_id,"x-client-secret":settings.cashfree_client_secret,"x-api-version":settings.cashfree_api_version,"Content-Type":"application/json"}
        body={"order_id":order_id,"order_amount":amount,"order_currency":"INR","customer_details":{"customer_id":customer_id,"customer_phone":phone or "9999999999"},"order_meta":{"return_url":settings.frontend_url+"/?order_id={order_id}","notify_url":settings.backend_url+"/api/webhooks/cashfree"}}
        async with httpx.AsyncClient(timeout=20) as client:
            response=await client.post(base+"/orders",json=body,headers=headers)
            response.raise_for_status(); return response.json()
