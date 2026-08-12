# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.2. Veri Standartlaştırma › 3.2.2.1. Z-Skoru Standartlaştırması
# Kitap  : Kod 3.21 (Z-skoru standartlaştırması)
# Dosya : bolum03/03_02_02_01_z-skoru-standartlastirmasi.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Z-Skoru Standartlaştırması ──────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy import stats

np.random.seed(42)
df = pd.DataFrame({
    "yas":         np.random.randint(18, 65, 300).astype(float),
    "gelir":       np.random.normal(50000, 15000, 300),
    "deneyim_yil": np.random.uniform(0, 40, 300),
    "kredi_skoru": np.random.randint(300, 850, 300).astype(float),
})

scaler = StandardScaler()
df_std = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# İstatistik doğrulama
print("=== Z-Skoru Standartlaştırması ===")
print(pd.DataFrame({
    "Orig Ort": df.mean().round(2),   "Orig Std": df.std().round(2),
    "Std Ort":  df_std.mean().round(6),"Std Std":  df_std.std().round(6),
}))

# Ampirik kural doğrulama
print("\nAmpirik Kural Doğrulama — gelir:")
z = df_std["gelir"]
for sinir, beklenen in [(1, 68.3), (2, 95.4), (3, 99.7)]:
    gercek = (z.abs() <= sinir).mean() * 100
    print(f"  |z| <= {sinir}: Beklenen ~%{beklenen:.1f}, Gerçek %{gercek:.1f}")

# Görselleştirme: histogram + standart normal eğrisi
fig, axes = plt.subplots(2, 4, figsize=(16, 7))
for i, col in enumerate(df.columns):
    axes[0,i].hist(df[col], bins=25, color="#3498db", alpha=0.7, density=True)
    axes[0,i].set_title(f"{col}\nOrijinal", fontsize=9)
    axes[1,i].hist(df_std[col], bins=25, color="#e74c3c", alpha=0.7, density=True)
    xr = np.linspace(-4,4,200)
    axes[1,i].plot(xr, stats.norm.pdf(xr), "k-", lw=2)
    axes[1,i].set_title(f"{col}\nZ-Skoru", fontsize=9)
plt.suptitle("Z-Skoru Standartlaştırması: Öncesi ve Sonrası", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.show()
