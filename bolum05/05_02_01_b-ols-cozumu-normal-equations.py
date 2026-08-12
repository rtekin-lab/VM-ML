# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.2. Regresyon Analizi: Klasikten Moderne › 5.2.1. Basit ve Çoklu Doğrusal Regresyon: OLS Yöntemi › B. OLS Çözümü: Normal Equations
# Kitap  : Kod 5.4 (Normal denklemlerle en küçük kareler çözümü)
# Dosya : bolum05/05_02_01_b-ols-cozumu-normal-equations.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn scipy statsmodels
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from scipy import stats

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
np.random.seed(42)
X, y = make_regression(n_samples=100, n_features=1, noise=15, random_state=42)
df = pd.DataFrame({'X': X.ravel(), 'Y': y})

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
print("═══ STATSMODELS — İstatistiksel Çıkarım ═══")
X_sm = sm.add_constant(df['X'])
model_sm = sm.OLS(df['Y'], X_sm).fit()
print(model_sm.summary())

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
print("\n═══ SKLEARN — Tahminleme ═══")
X_train, X_test, y_train, y_test = train_test_split(
    df[['X']], df['Y'], test_size=0.2, random_state=42)
model_sk = LinearRegression()
model_sk.fit(X_train, y_train)
y_pred = model_sk.predict(X_test)
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"Test R²: {r2_score(y_test, y_pred):.4f}")

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
# Diagnostics
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
residuals = df['Y'] - model_sm.fittedvalues

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
# Residual plot
axes[0,0].scatter(model_sm.fittedvalues, residuals, alpha=0.6)
axes[0,0].axhline(0, color='red', ls='--', lw=2)
axes[0,0].set_title('Residual Plot')

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
# Q-Q plot
stats.probplot(residuals, dist="norm", plot=axes[0,1])
axes[0,1].set_title('Q-Q Plot')

# --- ▌ Kod Örneği 5.2.1 — OLS: statsmodels vs sklearn ---
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "ols_diagnostics.png"), dpi=120)
print("\nDiagnostics: /tmp/ols_diagnostics.png")
