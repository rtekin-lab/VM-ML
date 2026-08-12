# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.2. Veri Standartlaştırma › 3.2.2.2. Robust Standartlaştırma (Medyan-IQR Tabanlı)
# Kitap  : Kod 3.22 (StandardScaler ile RobustScaler: aykırı değe)
# Dosya : bolum03/03_02_02_02_robust-standartlastirma.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Z-Skoru vs RobustScaler Karşılaştırması ─────────────────────
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler
import matplotlib.pyplot as plt

np.random.seed(42)
n = 200
# %5 aykırı değer
normal = np.random.normal(50, 10, int(n*0.95))
aykiri = np.random.uniform(150, 300, int(n*0.05))
x = np.concatenate([normal, aykiri]).reshape(-1, 1)

std_sc = StandardScaler().fit_transform(x)
rob_sc = RobustScaler().fit_transform(x)

# print header omitted
print("-"*46)
for m, v1, v2 in [
    ("Ortalama",  std_sc.mean(),       rob_sc.mean()),
    ("Medyan",    np.median(std_sc),   np.median(rob_sc)),
    ("Std Sapma", std_sc.std(),        rob_sc.std()),
    ("IQR",       np.percentile(std_sc,75)-np.percentile(std_sc,25),
                  np.percentile(rob_sc,75)-np.percentile(rob_sc,25)),
]:
    print(f"{m:<22} {v1:>12.4f} {v2:>12.4f}")
