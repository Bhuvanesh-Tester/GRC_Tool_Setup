import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routes import auth, policies, risks, compliance, workflows

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")

limiter = Limiter(key_func=lambda request: request.client.host)

app = FastAPI(title="GRC Platform API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(policies.router, prefix=api_prefix)
app.include_router(risks.router, prefix=api_prefix)
app.include_router(compliance.router, prefix=api_prefix)
app.include_router(workflows.router, prefix=api_prefix)

@app.get("/")
def root():
    return {"message": "GRC Platform API", "demo_mode": DEMO_MODE}