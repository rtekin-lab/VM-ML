# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.2. Regresyon Analizi: Klasikten Moderne › 5.2.3. Düzenlileştirme (Regularization): Ridge ve Lasso › C. Elastic Net
# Kitap  : Kod 5.5 (Ridge, Lasso ve Elastic Net katsayı yolların)
# Dosya : bolum05/05_02_03_c-elastic-net.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso, ElasticNet, RidgeCV, LassoCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
np.random.seed(42)
X, y = make_regression(n_samples=100, n_features=50, n_informative=10, noise=20)

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
models = {
    'Ridge(α=1)': Ridge(alpha=1.0),
    'Ridge(α=10)': Ridge(alpha=10.0),
    'Lasso(α=0.1)': Lasso(alpha=0.1),
    'Lasso(α=1)': Lasso(alpha=1.0),
    'ElasticNet': ElasticNet(alpha=0.5, l1_ratio=0.5)
}

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
for name, model in models.items():
    model.fit(X_train_s, y_train)
    score = model.score(X_test_s, y_test)
    n_nonzero = np.sum(np.abs(model.coef_) > 1e-5)
    print(f"{name:15} | R²={score:.3f} | Non-zero={n_nonzero}/50")

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
# Optimal α selection
alphas = np.logspace(-2, 4, 50)
ridge_cv = RidgeCV(alphas=alphas, cv=5)
ridge_cv.fit(X_train_s, y_train)
print(f"\nRidge optimal α: {ridge_cv.alpha_:.4f}")

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
lasso_cv = LassoCV(alphas=np.logspace(-4, 1, 50), cv=5)
lasso_cv.fit(X_train_s, y_train)
print(f"Lasso optimal α: {lasso_cv.alpha_:.4f}")
print(f"Lasso selected: {np.sum(np.abs(lasso_cv.coef_)>1e-5)}/50 features")

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
# Regularization path
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
coefs_ridge, coefs_lasso = [], []
for alpha in alphas:
    coefs_ridge.append(Ridge(alpha=alpha).fit(X_train_s, y_train).coef_)
    coefs_lasso.append(Lasso(alpha=alpha).fit(X_train_s, y_train).coef_)

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
for i in range(10):
    ax1.plot(alphas, [c[i] for c in coefs_ridge], alpha=0.7)
    ax2.plot(alphas, [c[i] for c in coefs_lasso], alpha=0.7)

# --- ▌ Kod Örneği 5.2.3 — Ridge, Lasso, ElasticNet Karşılaştırma ---
ax1.set_xscale('log'); ax2.set_xscale('log')
ax1.set_title('Ridge Path'); ax2.set_title('Lasso Path (Sparse)')
for ax in [ax1, ax2]:
    ax.set_xlabel('α'); ax.set_ylabel('Coefficient'); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "regularization_path.png"), dpi=120)
print("Saved: /tmp/regularization_path.png")
