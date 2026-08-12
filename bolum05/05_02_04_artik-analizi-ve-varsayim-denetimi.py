# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: Makine Öğrenmesine Giriş ve Regresyon Analizi › 5.2. Regresyon Analizi › 5.2.4. Model Varsayımlarının Denetimi
# Dosya : bolum05/05_02_04_artik-analizi-ve-varsayim-denetimi.py
# Gerekli: pip install numpy matplotlib scikit-learn scipy
# ==========================================================================
"""Doğrusal regresyon varsayımlarının artık (residual) grafikleriyle denetimi."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
n = 200
X = rng.uniform(0, 10, (n, 1))

# İki senaryo: varsayımları sağlayan ve sağlamayan veri
y_iyi = 3 + 2.2 * X[:, 0] + rng.normal(0, 1.5, n)                 # sabit varyans
y_kotu = 3 + 2.2 * X[:, 0] + rng.normal(0, 0.4 * X[:, 0] + 0.2, n)  # varyans x ile büyüyor

fig, axes = plt.subplots(2, 3, figsize=(14, 7))
for satir, (y, etiket) in enumerate([(y_iyi, "Varsayımlar sağlanıyor"),
                                     (y_kotu, "Değişen varyans (heteroskedastisite)")]):
    model = LinearRegression().fit(X, y)
    tahmin = model.predict(X)
    artik = y - tahmin
    std_artik = artik / artik.std()

    # 1. Artık - tahmin grafiği: rastgele dağılım beklenir
    ax = axes[satir, 0]
    ax.scatter(tahmin, artik, s=14, alpha=0.6, color="#2E5A8A")
    ax.axhline(0, color="#C0392B", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Tahmin edilen değer"); ax.set_ylabel("Artık")
    ax.set_title(f"Artık - Tahmin\n{etiket}", fontsize=9)

    # 2. Q-Q grafiği: artıkların normalliği
    ax = axes[satir, 1]
    stats.probplot(std_artik, dist="norm", plot=ax)
    ax.set_title("Artıkların Q-Q grafiği", fontsize=9)
    ax.get_lines()[0].set_markersize(3)

    # 3. Ölçek-konum grafiği: varyans sabitliği
    ax = axes[satir, 2]
    ax.scatter(tahmin, np.sqrt(np.abs(std_artik)), s=14, alpha=0.6, color="#27AE60")
    ax.set_xlabel("Tahmin edilen değer"); ax.set_ylabel("√|standart artık|")
    ax.set_title("Ölçek - konum", fontsize=9)

plt.tight_layout()
plt.show()

# Breusch-Pagan benzeri basit sınama: artık karesi ile tahmin arasındaki ilişki
for y, etiket in [(y_iyi, "sağlanıyor"), (y_kotu, "sağlanmıyor")]:
    model = LinearRegression().fit(X, y)
    artik = y - model.predict(X)
    r, p = stats.pearsonr(model.predict(X), np.abs(artik))
    print(f"Varsayım {etiket:12s} | |artık| ~ tahmin korelasyonu r={r:+.3f}, p={p:.4f}")
