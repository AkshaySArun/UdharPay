from collections import defaultdict,deque
from threading import Lock
from time import monotonic
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Small per-process sliding-window guard; use a shared store for multi-worker deployments."""
    def __init__(self,app):
        super().__init__(app); self.events=defaultdict(deque); self.lock=Lock()
    async def dispatch(self,request:Request,call_next):
        path=request.url.path; method=request.method.upper()
        if method in {"POST","PUT","DELETE"} and path.startswith("/api/"):
            if path.endswith("/auth/register"): limit,window=5,3600
            elif path.endswith("/auth/login"): limit,window=10,60
            elif "/sarvam/" in path or path.endswith("/khata/upload"): limit,window=20,60
            else: limit,window=120,60
            client=request.client.host if request.client else "unknown"
            key=(client,path); now=monotonic()
            with self.lock:
                events=self.events[key]
                while events and now-events[0]>=window: events.popleft()
                if len(events)>=limit: return JSONResponse({"detail":"Too many requests. Please wait and try again."},status_code=429,headers={"Retry-After":str(max(1,int(window-(now-events[0]))) if events else window)})
                events.append(now)
                if len(self.events)>4096:
                    for old_key,queue in list(self.events.items()):
                        while queue and now-queue[0]>=3600: queue.popleft()
                        if not queue: self.events.pop(old_key,None)
        return await call_next(request)
