# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.6. İleri Düzey Ölçeklendirme: QuantileTransformer ve Batch Normalizasyon › 3.2.6.1. Quantile Dönüşümü
# Kitap  : Kod 3.26 (QuantileTransformer ile uniform ve normal he)
# Dosya : bolum03/03_02_06_01_quantile-donusumu.py
# Gerekli: pip install matplotlib numpy scikit-learn scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── QuantileTransformer ─────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import QuantileTransformer
from scipy import stats

np.random.seed(42)
n = 1000
X = np.column_stack([
    np.random.lognormal(0, 1, n),   # Sağa çarpık
    np.random.exponential(2, n),    # Üstel
    stats.chi2.rvs(df=5, size=n),   # Ki-kare
])

qt_u = QuantileTransformer(output_distribution="uniform", n_quantiles=100, random_state=42)
qt_n = QuantileTransformer(output_distribution="normal",  n_quantiles=100, random_state=42)
X_u = qt_u.fit_transform(X)
X_n = qt_n.fit_transform(X)

isimler = ["Log-Normal", "Üstel", "Ki-kare"]
print("Normallik testi (Shapiro, n=200 alt örnek):")
# print header omitted
idx = np.random.choice(n, 200, replace=False)
for i, isim in enumerate(isimler):
    _, po = stats.shapiro(X[idx, i])
    _, pu = stats.shapiro(X_u[idx, i])
    _, pn = stats.shapiro(X_n[idx, i])
    print(f"{isim:<12} {po:>12.6f} {pu:>12.6f} {pn:>12.6f}")
