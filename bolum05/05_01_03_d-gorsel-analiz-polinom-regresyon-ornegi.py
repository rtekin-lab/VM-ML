# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.1. Makine Öğrenmesi Paradigması › 5.1.3. Bias-Variance Takası: Aşırı/Eksik Öğrenme Dengesi › D. Görsel Analiz: Polinom Regresyon Örneği
# Kitap  : Kod 5.3 (Polinom regresyonla eksik ve aşırı öğrenmeni)
# Dosya : bolum05/05_01_03_d-gorsel-analiz-polinom-regresyon-ornegi.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

np.random.seed(42)

# ════════════════════════════════════════════════════════════════════════════
# A. SENTETİK VERİ: Gerçek fonksiyon + gürültü
# ════════════════════════════════════════════════════════════════════════════

# Gerçek fonksiyon: f(x) = x·sin(x)
n_samples = 50
X = np.sort(np.random.uniform(0, 10, n_samples))
y_true = X * np.sin(X)
noise = np.random.normal(0, 1.5, n_samples)
y = y_true + noise

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Görselleştirme için yoğun grid
X_plot = np.linspace(0, 10, 500)
y_plot_true = X_plot * np.sin(X_plot)

# ════════════════════════════════════════════════════════════════════════════
# B. FARKLI POLİNOM DERECELERİ: d = 1, 3, 5, 15
# ════════════════════════════════════════════════════════════════════════════

degrees = [1, 3, 5, 15]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()

train_errors = []
test_errors = []

for idx, degree in enumerate(degrees):
    ax = axes[idx]

    # Polinom öznitelikler
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train.reshape(-1, 1))
    X_test_poly = poly.transform(X_test.reshape(-1, 1))
    X_plot_poly = poly.transform(X_plot.reshape(-1, 1))

    # Model eğitimi
    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    # Tahminler
    y_train_pred = model.predict(X_train_poly)
    y_test_pred = model.predict(X_test_poly)
    y_plot_pred = model.predict(X_plot_poly)

    # Hatalar
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    train_errors.append(train_mse)
    test_errors.append(test_mse)

    # Görselleştirme
    ax.scatter(X_train, y_train, color='blue', s=40, alpha=0.6, label='Train')
    ax.scatter(X_test, y_test, color='red', s=40, alpha=0.6, label='Test')
    ax.plot(X_plot, y_plot_true, 'k--', lw=1.5, alpha=0.5, label='Gerçek Fonksiyon')
    ax.plot(X_plot, y_plot_pred, 'g-', lw=2.5, label=f'Polinom (d={degree})')

    # Durum etiketi
    if degree == 1:
        durum = "UNDERFITTING"
        renk = 'orange'
    elif degree in [3, 5]:
        durum = "İYİ FIT"
        renk = 'green'
    else:
        durum = "OVERFITTING"
        renk = 'red'

    ax.text(0.5, 0.95, durum, transform=ax.transAxes, fontsize=12,
            fontweight='bold', color=renk, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_title(f'Derece={degree}  |  Train MSE={train_mse:.2f}, Test MSE={test_mse:.2f}',
                 fontweight='bold', fontsize=10)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.legend(loc='lower left', fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(-12, 12)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "bias_variance_polynomial.png"), dpi=120, bbox_inches='tight')
plt.close()

# ════════════════════════════════════════════════════════════════════════════
# C. BIAS-VARIANCE AYRIŞIMI GRAFİĞİ
# ════════════════════════════════════════════════════════════════════════════

# Daha geniş derece aralığı
degrees_full = range(1, 21)
train_errors_full = []
test_errors_full = []

for d in degrees_full:
    poly = PolynomialFeatures(degree=d, include_bias=False)
    X_tr_p = poly.fit_transform(X_train.reshape(-1, 1))
    X_te_p = poly.transform(X_test.reshape(-1, 1))

    model = LinearRegression()
    model.fit(X_tr_p, y_train)

    train_errors_full.append(mean_squared_error(y_train, model.predict(X_tr_p)))
    test_errors_full.append(mean_squared_error(y_test, model.predict(X_te_p)))

# Bias-Variance teorik eğrileri (illustrative)
bias_squared = np.linspace(20, 0.5, 20)   # Bias azalır
variance = np.linspace(0.5, 25, 20)        # Variance artar
total_error_theory = bias_squared + variance

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Sol: Gerçek Train/Test hataları
ax1.plot(degrees_full, train_errors_full, 'bo-', lw=2, label='Train MSE', markersize=6)
ax1.plot(degrees_full, test_errors_full, 'rs-', lw=2, label='Test MSE', markersize=6)
optimal_idx = np.argmin(test_errors_full)
ax1.axvline(degrees_full[optimal_idx], color='green', ls='--', lw=2,
            label=f'Optimal d={degrees_full[optimal_idx]}')
ax1.set_xlabel('Polinom Derecesi (Model Karmaşıklığı)', fontsize=12)
ax1.set_ylabel('MSE', fontsize=12)
ax1.set_title('Model Karmaşıklığı vs Hata', fontweight='bold')
ax1.legend(); ax1.grid(alpha=0.3)

# Sağ: Teorik Bias-Variance ayrışımı
ax2.plot(degrees_full, bias_squared, 'r-', lw=2.5, label='Bias²')
ax2.plot(degrees_full, variance, 'b-', lw=2.5, label='Variance')
ax2.plot(degrees_full, total_error_theory, 'k-', lw=3, label='Toplam Hata (Bias²+Var)')
ax2.axvline(degrees_full[np.argmin(total_error_theory)], color='green', ls='--', lw=2,
            label='Optimal Nokta')
ax2.fill_between(degrees_full, 0, total_error_theory, where=(np.array(degrees_full) < 5),
                  alpha=0.2, color='orange', label='Underfitting Bölgesi')
ax2.fill_between(degrees_full, 0, total_error_theory, where=(np.array(degrees_full) > 12),
                  alpha=0.2, color='red', label='Overfitting Bölgesi')
ax2.set_xlabel('Model Karmaşıklığı', fontsize=12)
ax2.set_ylabel('Hata Bileşenleri', fontsize=12)
ax2.set_title('Bias-Variance Trade-off (Teorik)', fontweight='bold')
ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "bias_variance_tradeoff.png"), dpi=120, bbox_inches='tight')
plt.close()

print("═══ BIAS-VARIANCE ANALİZİ ═══")
print(f"Polinom d=1  (Underfitting) → Train MSE={train_errors[0]:.2f}, Test MSE={test_errors[0]:.2f}")
print(f"Polinom d=3  (İyi Fit)      → Train MSE={train_errors[1]:.2f}, Test MSE={test_errors[1]:.2f}")
print(f"Polinom d=15 (Overfitting)  → Train MSE={train_errors[3]:.2f}, Test MSE={test_errors[3]:.2f}")
print(f"\nOptimal derece: {degrees_full[optimal_idx]} (Test MSE minimum)")
print("\nGrafikler: /tmp/bias_variance_polynomial.png, /tmp/bias_variance_tradeoff.png")
