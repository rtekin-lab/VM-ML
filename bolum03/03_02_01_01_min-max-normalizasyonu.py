# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.1. Veri Normalizasyonu › 3.2.1.1. Min-Max Normalizasyonu (Lineer Ölçekleme)
# Kitap  : Kod 3.17 (MinMaxScaler ile [0,1] ve [-1,1] aralığına n)
# Dosya : bolum03/03_02_01_01_min-max-normalizasyonu.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Min-Max Normalizasyonu ──────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

np.random.seed(42)
df = pd.DataFrame({
    "yas":        np.random.randint(18, 65, 200).astype(float),
    "gelir":      np.random.normal(35000, 12000, 200),
    "kredi_skoru":np.random.randint(300, 850, 200).astype(float),
    "deneyim":    np.random.uniform(0, 40, 200),
})

# [0,1] ve [-1,1] aralıklarına normalizasyon
scaler01 = MinMaxScaler(feature_range=(0, 1))
scaler11 = MinMaxScaler(feature_range=(-1, 1))
df_n01 = pd.DataFrame(scaler01.fit_transform(df), columns=df.columns)
df_n11 = pd.DataFrame(scaler11.fit_transform(df), columns=df.columns)

# İstatistik karşılaştırması
print("=== [0,1] Normalizasyon Sonucu ===")
print(pd.DataFrame({
    "Orig Min": df.min().round(2),  "Orig Max": df.max().round(2),
    "Norm Min": df_n01.min().round(4), "Norm Max": df_n01.max().round(4),
}))

# Geri dönüşüm doğrulaması
df_geri = pd.DataFrame(scaler01.inverse_transform(df_n01), columns=df.columns)
print("\nGeri dönüşüm max mutlak hata:", (df - df_geri).abs().max().round(8).max())

# Aykırı değer etkisi
x_norm = np.array([10, 20, 30, 40, 500]).reshape(-1, 1)  # 500 aykırı
print("\nAykırı değer etkisi Min-Max:", MinMaxScaler().fit_transform(x_norm).ravel())
