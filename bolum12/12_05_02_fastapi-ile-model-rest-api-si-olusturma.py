# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.5. Derin Öğrenme Modellerini Ölçeklendirme ve Dağıtım (Deployment) › 12.5.2. Bulut Bilişim ve Üretim Ortamı (Production Deployment) › FastAPI ile Model REST API'si Oluşturma
# Kitap  : Kod 12.12 (Üretim ortamı için bağımlılık listesi)
# Dosya : bolum12/12_05_02_fastapi-ile-model-rest-api-si-olusturma.py
# Gerekli: pip install fastapi numpy pydantic tensorflow uvicorn
# ==========================================================================
# requirements.txt:
# fastapi uvicorn tensorflow pydantic numpy pillow

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import time
import logging
from typing import List, Optional

# ─────────────────────────────────────────────────────────────────────
# Uygulama Yaşam Döngüsü: Model Başlangıçta Yüklenir
# ─────────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model değişkeni
model_registry = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI başladığında modeli yükle; kapanırken temizle."""
    logger.info("Model yükleniyor...")
    try:
        model_registry["cifar10"] = tf.keras.models.load_model("best_model.keras")
        logger.info(f"Model başarıyla yüklendi: {model_registry['cifar10'].name}")
    except Exception as e:
        logger.error(f"Model yüklenemedi: {e}")
        raise
    yield   # Burada uygulama çalışır
    model_registry.clear()
    logger.info("Model bellekten temizlendi.")

app = FastAPI(
    title="CIFAR-10 Görüntü Sınıflandırma API",
    description="ResNet50 tabanlı derin öğrenme modeli ile görüntü sınıflandırma",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────
# Veri Modelleri (Pydantic)
# ─────────────────────────────────────────────────────────────────────

CIFAR10_CLASSES = ["uçak", "otomobil", "kuş", "kedi", "geyik",
                   "köpek", "kurbağa", "at", "gemi", "kamyon"]

class Prediction(BaseModel):
    sinif: str = Field(..., description="Tahmin edilen sınıf adı")
    sinif_id: int = Field(..., description="Sınıf indeksi")
    guven: float = Field(..., description="Güven skoru (0-1)")
    tum_olasiliklar: List[float] = Field(..., description="Tüm sınıfların olasılıkları")
    gecikme_ms: float = Field(..., description="Çıkarım süresi (milisaniye)")

class HealthResponse(BaseModel):
    durum: str
    model_yuklu: bool
    tensorflow_surumu: str

# ─────────────────────────────────────────────────────────────────────
# API Endpoint'leri
# ─────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["Sistem"])
async def health_check():
    """Servis sağlık kontrolü."""
    return HealthResponse(
        durum="aktif",
        model_yuklu="cifar10" in model_registry,
        tensorflow_surumu=tf.__version__
    )

@app.post("/predict/image", response_model=Prediction, tags=["Tahmin"])
async def predict_image(file: UploadFile = File(...)):
    """
    Görüntü dosyası yükleyerek sınıflandırma yap.
    Desteklenen formatlar: JPEG, PNG, BMP
    """
    if "cifar10" not in model_registry:
        raise HTTPException(status_code=503, detail="Model henüz hazır değil")

    # Dosya türü kontrolü
    if file.content_type not in ["image/jpeg", "image/png", "image/bmp"]:
        raise HTTPException(status_code=400,
            detail=f"Desteklenmeyen dosya türü: {file.content_type}")

    try:
        # Görüntüyü oku ve önişle
        content = await file.read()
        image   = Image.open(io.BytesIO(content)).convert("RGB")
        image   = image.resize((32, 32))  # CIFAR-10 boyutu
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # (1, 32, 32, 3)

        # Tahmin
        model = model_registry["cifar10"]
        start = time.perf_counter()
        probs = model.predict(img_array, verbose=0)[0]
        elapsed_ms = (time.perf_counter() - start) * 1000

        best_idx = int(np.argmax(probs))
        return Prediction(
            sinif=CIFAR10_CLASSES[best_idx],
            sinif_id=best_idx,
            guven=float(probs[best_idx]),
            tum_olasiliklar=[float(p) for p in probs],
            gecikme_ms=round(elapsed_ms, 2)
        )
    except Exception as e:
        logger.error(f"Tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", tags=["Tahmin"])
async def predict_batch(files: List[UploadFile] = File(...)):
    """Çoklu görüntü için batch tahmin."""
    if len(files) > 32:
        raise HTTPException(400, "Tek seferde en fazla 32 görüntü")

    results = []
    for f in files:
        try:
            pred = await predict_image(f)
            results.append({"dosya": f.filename, "tahmin": pred})
        except Exception as e:
            results.append({"dosya": f.filename, "hata": str(e)})
    return {"sonuclar": results, "toplam": len(results)}

# Çalıştırma: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
