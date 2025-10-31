from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import chat, status, audio, reset, auth
from app.utils.firebase import init_firebase
app = FastAPI(
    title=settings.app_name,
    description="Sistema Digital de Alimentação - API",
    version="1.0.0",
    debug=settings.debug,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    init_firebase()
except Exception as e:
    print(f"⚠️ Firebase não inicializado: {e}")
    print("Configure FIREBASE_CREDENTIALS_PATH ou FIREBASE_CREDENTIALS_JSON no .env")
app.include_router(auth.router)
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(audio.router, prefix="/api", tags=["audio"])
app.include_router(reset.router, prefix="/api", tags=["reset"])
@app.get("/")
async def root():
    return {"message": "SDA API - Sistema Digital de Alimentação", "status": "running"}
@app.get("/health")
async def health():
    return {"status": "healthy"}