from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from tinydb import TinyDB, Query
import datetime

app = FastAPI()
db = TinyDB('db.json') # Veri güvenliği burada başlıyor

# Middleware: Gelen her isteği "Sovereign" gözüyle süzer
@app.middleware("http")
async def sovereign_protection(request: Request, call_next):
    # 1. Adım: Bot Kontrolü (Sovereign Core Mantığı)
    user_agent = request.headers.get("user-agent", "").lower()
    if "bot" in user_agent or "python" in user_agent:
        return Response(content="Access Denied", status_code=403)
    
    # 2. Adım: Consent Mode V2 "Pasaport" Kontrolü
    # Kullanıcıdan çerez onayı gelip gelmediğini kontrol ederiz
    consent_status = request.cookies.get("consent_status", "denied")
    
    response = await call_next(request)
    
    # Header'lara Consent Sinyalini ekle (Google Analytics'e iletilecek)
    response.headers["X-Consent-Status"] = consent_status
    return response

@app.get("/")
async def root():
    # Burada Consent Mode V2 banner'ı olan ana sayfamız dönecek
    return HTMLResponse(content="""
        <html>
            <body>
                <h1>Smyrna & Sable - Güvenli Alışveriş Kapısı</h1>
                <p>Burada Consent Mode V2 aktif.</p>
                <!-- Çerez Onay Banner'ı buraya gelecek -->
            </body>
        </html>
    """)

@app.get("/health")
async def health():
    return {"status": "Sovereign Core Active", "timestamp": datetime.datetime.now()}