# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.3. Güç Dönüşümleri ve Dağılım Şekillendirme › 3.2.3.2. Box-Cox ve Yeo-Johnson Dönüşümleri
# Kitap  : Kod 3.24 (Logaritma, Box-Cox ve Yeo-Johnson dönüşümler)
# Dosya : bolum03/03_02_03_02_box-cox-ve-yeo-johnson-donusumleri.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Log, Box-Cox ve Yeo-Johnson Dönüşümleri ────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PowerTransformer
from scipy import stats

np.random.seed(42)
gelir = np.random.lognormal(mean=10.5, sigma=0.8, size=500)

# Log dönüşümü
log_gelir = np.log(gelir)

# Box-Cox (yalnızca pozitif)
pt_bc = PowerTransformer(method="box-cox")
bc_gelir = pt_bc.fit_transform(gelir.reshape(-1,1)).ravel()

# Yeo-Johnson
pt_yj = PowerTransformer(method="yeo-johnson")
yj_gelir = pt_yj.fit_transform(gelir.reshape(-1,1)).ravel()

print(f"Box-Cox lambda   : {pt_bc.lambdas_[0]:.4f}")
print(f"Yeo-Johnson lambda: {pt_yj.lambdas_[0]:.4f}")

# Normallik testleri
print("\nNormallik Testleri (Shapiro-Wilk):")
idx = np.random.choice(500, 200, replace=False)
for isim, dizi in [("Orijinal", gelir[idx]), ("Log", log_gelir[idx]),
                    ("Box-Cox", bc_gelir[idx]), ("Yeo-Johnson", yj_gelir[idx])]:
    _, p = stats.shapiro(dizi)
    print(f"  {isim:<15}: p={p:.4f}  çarpıklık={stats.skew(dizi):.4f}")

# Görselleştirme
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
donusumler = [("Orijinal", gelir), ("log(x)", log_gelir),
              ("Box-Cox", bc_gelir), ("Yeo-Johnson", yj_gelir)]
for i, (isim, dizi) in enumerate(donusumler):
    axes[0,i].hist(dizi, bins=40, color="#3498db", alpha=0.7, density=True)
    axes[0,i].set_title(f"{isim}\nÇarp.:{stats.skew(dizi):.3f}", fontsize=9)
    stats.probplot(dizi, dist="norm", plot=axes[1,i])
    axes[1,i].set_title(f"Q-Q: {isim}", fontsize=9)
plt.suptitle("Güç Dönüşümleri: Normalliğe Yaklaştırma", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.show()
