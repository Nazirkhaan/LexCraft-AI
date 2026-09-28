from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .brand import APP_NAME, APP_TAGLINE
from .routes import router

app = FastAPI(
    title=f"{APP_NAME} API",
    version="2.0.0",
    description=f"{APP_TAGLINE} - generate, preview, edit and export legal documents",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"service": APP_NAME, "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
