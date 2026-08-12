# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.4. Matplotlib — Veri Görselleştirme Kütüphanesi › C. Temel Görselleştirme Örnekleri
# Kitap  : Kod 1.30 (Temel Görselleştirme örnekleri) · Kod 1.31 (Çarpık dağılım) · Kod 1.32 (Temel Görselleştirme örnekleri) · Kod 1.33 (Scatter Plot ve Korelasyon) · Kod 1.34 (Korelasyon katsayısı: r = Σ(xi-x̄)(yi-ȳ) / √) · Kod 1.35 (Temel Görselleştirme örnekleri) · Kod 1.36 (Temel Görselleştirme örnekleri)
# Dosya : bolum01/01_02_04_c-temel-gorsellestirme-ornekleri.py
# Gerekli: pip install matplotlib numpy scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import matplotlib.pyplot as plt
import numpy as np

# ─── 1. Dağılım ve Histogram ─────────────────────────────────────────────────
np.random.seed(42)
normal_veri   = np.random.normal(100, 15, 1000)
carpik_veri   = np.random.exponential(scale=20, size=1000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram + KDE yaklaşımı
axes[0].hist(normal_veri, bins=40, density=True, alpha=0.7,
             color='steelblue', edgecolor='white', label='Normal N(100,15²)')
# Manuel KDE çizgisi
x_range = np.linspace(40, 160, 300)
from scipy.stats import norm
axes[0].plot(x_range, norm.pdf(x_range, 100, 15),
             'r-', lw=2.5, label='Teorik PDF')
axes[0].set_title('Normal Dağılım: N(100, 225)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Değer')
axes[0].set_ylabel('Yoğunluk')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Çarpık dağılım
axes[1].hist(carpik_veri, bins=40, density=True, alpha=0.7,
             color='coral', edgecolor='white', label='Üstel (λ=0.05)')
axes[1].set_title('Çarpık Dağılım: Exp(20)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Değer')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/dagilim_gorseli.png', dpi=120, bbox_inches='tight')
plt.close()
print("Grafik kaydedildi: dagilim_gorseli.png")

# ─── 2. Scatter Plot ve Korelasyon ───────────────────────────────────────────
n = 200
x = np.random.randn(n) * 10 + 50       # Gelir benzeri değişken
y = 0.6 * x + np.random.randn(n) * 5 + 20  # Korelasyonlu değişken

# Korelasyon katsayısı: r = Σ(xi-x̄)(yi-ȳ) / √[Σ(xi-x̄)² · Σ(yi-ȳ)²]
r = np.corrcoef(x, y)[0, 1]

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(x, y, c=y, cmap='viridis', alpha=0.7, s=50, edgecolors='w', lw=0.5)

# Regresyon doğrusu
m, b = np.polyfit(x, y, 1)
x_hat = np.linspace(x.min(), x.max(), 100)
ax.plot(x_hat, m * x_hat + b, 'r--', lw=2, label=f'y = {m:.2f}x + {b:.2f}')

plt.colorbar(scatter, ax=ax, label='y değeri')
ax.set_title(f'Scatter Plot — Pearson r = {r:.3f}', fontsize=13, fontweight='bold')
ax.set_xlabel('X değişkeni')
ax.set_ylabel('Y değişkeni')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/claude/scatter_korelasyon.png', dpi=120, bbox_inches='tight')
plt.close()
print(f"Korelasyon katsayısı r = {r:.3f}")
