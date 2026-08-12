# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.5. Derin Öğrenme Modellerini Ölçeklendirme ve Dağıtım (Deployment) › 12.5.2. Bulut Bilişim ve Üretim Ortamı (Production Deployment) › Docker ile Konteynerizasyon
# Kitap  : Kod 12.13 (Model servisi için Docker imajı tanımı)
# Dosya : bolum12/12_05_02_docker-ile-konteynerizasyon.py
# Gerekli: pip install numpy requests scipy tensorflow
# ==========================================================================
# ─── Dockerfile ─────────────────────────────────────────────────────
# FROM tensorflow/tensorflow:2.15.0-gpu
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8000
# HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
#   CMD curl -f http://localhost:8000/health || exit 1
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# ─────────────────────────────────────────────────────────────────────
# Docker Build ve Çalıştırma
# ─────────────────────────────────────────────────────────────────────

# docker build -t cifar10-api:v1.0 .
# docker run -d --gpus all -p 8000:8000 --name cifar10-api cifar10-api:v1.0

# ─────────────────────────────────────────────────────────────────────
# TensorFlow Serving ile Yüksek Performanslı Deployment
# ─────────────────────────────────────────────────────────────────────

import tensorflow as tf
import subprocess
import requests
import json
import numpy as np

# Model SavedModel formatında kaydet (TF Serving için zorunlu)
model = tf.keras.models.load_model("best_model.keras")
model.save("models/cifar10/1")   # Sürüm klasörü: 1, 2, 3...
print("Model SavedModel formatında kaydedildi.")

# ─────────────────────────────────────────────────────────────────────
# docker run -d --name tfserving \
#   -p 8501:8501 \
#   -v /path/to/models:/models \
#   tensorflow/serving \
#   --model_config_file=/models/models.config
# ─────────────────────────────────────────────────────────────────────

# TF Serving REST API test
def predict_via_tfserving(images: np.ndarray, server="localhost:8501") -> dict:
    """TF Serving REST API üzerinden tahmin."""
    url = f"http://{server}/v1/models/cifar10:predict"
    payload = {"instances": images.tolist()}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

# Örnek istek
test_input = np.random.rand(1, 32, 32, 3).astype("float32")
# result = predict_via_tfserving(test_input)
# print(f"TF Serving yanıtı: {result}")

# ─────────────────────────────────────────────────────────────────────
# A/B Test Simülasyonu: Model v1 vs v2
# ─────────────────────────────────────────────────────────────────────

import random

def ab_test_predict(features: np.ndarray, traffic_split_v2: float = 0.1):
    """
    Canary deployment: %10 trafiği v2'ye yönlendir, %90 v1'e.
    Gerçek sistemde bu Istio veya Nginx ile ağ katmanında yapılır.
    """
    if random.random() < traffic_split_v2:
        model_version = "v2"
        # result = predict_via_tfserving(features, "v2-server:8501")
    else:
        model_version = "v1"
        # result = predict_via_tfserving(features, "v1-server:8501")

    # Metrikleri kaydet (MLflow veya Prometheus)
    # metrics_logger.log({"version": model_version, "latency": latency})
    return model_version

print("API, TF Serving ve A/B test altyapısı hazır.")

# ─────────────────────────────────────────────────────────────────────
# Model İzleme (Monitoring): Veri Kayması (Data Drift) Tespiti
# ─────────────────────────────────────────────────────────────────────

from scipy import stats

def detect_data_drift(reference_data: np.ndarray,
                      current_data:   np.ndarray,
                      threshold: float = 0.05) -> dict:
    """
    KS-testi ile veri kayması tespiti.
    p-değeri < threshold ise kayma var demektir.
    """
    drift_report = {}
    for i in range(reference_data.shape[1]):
        ks_stat, p_val = stats.ks_2samp(reference_data[:, i], current_data[:, i])
        drift_report[f"ozellik_{i}"] = {
            "ks_istatistigi": round(ks_stat, 4),
            "p_degeri":       round(p_val, 4),
            "drift_var":      p_val < threshold
        }
    drifted = sum(1 for v in drift_report.values() if v["drift_var"])
    drift_report["ozet"] = {
        "toplam_ozellik": reference_data.shape[1],
        "drift_ozellik":  drifted,
        "drift_orani":    round(drifted / reference_data.shape[1], 3)
    }
    return drift_report

# Örnek kullanım
ref  = np.random.randn(1000, 20)   # Eğitim verisi dağılımı
curr = np.random.randn(200, 20)    # Üretim verisi (normal)
drifted_curr = ref + np.random.randn(200, 20) * 3  # Yüksek drift

report_normal  = detect_data_drift(ref, curr)
report_drifted = detect_data_drift(ref, drifted_curr)

print(f"Normal veri  – Drift eden özellik: {report_normal['ozet']['drift_ozellik']}")
print(f"Drifted veri – Drift eden özellik: {report_drifted['ozet']['drift_ozellik']}")
