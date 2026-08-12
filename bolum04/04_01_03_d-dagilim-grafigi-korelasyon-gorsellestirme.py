# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.3. Temel Grafik Türleri: Matematiksel Temel ve Uygulamalar › D. Dağılım Grafiği: Korelasyon Görselleştirme
# Dosya : bolum04/04_01_03_d-dagilim-grafigi-korelasyon-gorsellestirme.py
# Gerekli: pip install matplotlib numpy scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

np.random.seed(42)

# ─── A. Çizgi Grafiği: Zaman Serisi ──────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

t = np.linspace(0, 365, 365)
seri = 50 + 0.05*t + 10*np.sin(2*np.pi*t/365) + np.random.normal(0,2,365)
MA30 = np.convolve(seri, np.ones(30)/30, mode='same')

axes[0].plot(t, seri, alpha=0.5, color='#A8C6E8', lw=1.0, label='Gözlem')
axes[0].plot(t, MA30, color='#1E3A5F', lw=2.5, label='30-günlük Ort.')
axes[0].fill_between(t, MA30-5, MA30+5, alpha=0.15, color='#2E5F8A', label='±5 bantı')
axes[0].set_title('Zaman Serisi: Trend + Mevsimsellik', fontweight='bold')
axes[0].set_xlabel('Gün'); axes[0].set_ylabel('Değer')
axes[0].legend(loc='upper left', fontsize=9)

# Log-log çizgi grafiği
x_log = np.logspace(0, 3, 100)
axes[1].loglog(x_log, x_log**1.5, 'b-', lw=2, label='y = x^1.5')
axes[1].loglog(x_log, 50*x_log**0.5, 'r--', lw=2, label='y = 50√x')
axes[1].loglog(x_log, 1000/x_log, 'g:', lw=2, label='y = 1000/x')
axes[1].set_title('Log-Log Grafiği', fontweight='bold')
axes[1].legend(); axes[1].grid(True, which='both', alpha=0.4)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "cizgi.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── B. Histogram: PDF + KDE ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

mu, sigma = 50, 10; n = 1000
veri = np.random.normal(mu, sigma, n)

# Histogram + teorik PDF
axes[0].hist(veri, bins=40, density=True, color='#2E5F8A', alpha=0.7, edgecolor='white')
x_pdf = np.linspace(mu-4*sigma, mu+4*sigma, 200)
axes[0].plot(x_pdf, stats.norm.pdf(x_pdf, mu, sigma), 'r-', lw=2.5, label=f'N({mu},{sigma})')
axes[0].axvline(veri.mean(), color='darkred', ls='--', lw=1.5, label='x̄')
axes[0].set_title('Normal Dağılım + Teorik PDF', fontweight='bold')
axes[0].legend(fontsize=9)

# Farklı bin sayıları
sturges = int(1 + np.log2(n))
for b, c in zip([5, sturges, 60, 'auto'], ['#C44D34','#1E3A5F','#2E8B57','#8B4513']):
    axes[1].hist(veri, bins=b, density=True, alpha=0.4, edgecolor='white',
                 label=f'bins={b}')
axes[1].set_title(f'Bin Sayısı Karşılaştırması\n(Sturges k={sturges})', fontweight='bold')
axes[1].legend(fontsize=9)

# Bimodal + KDE
veri_bi = np.concatenate([np.random.normal(-2,0.8,400), np.random.normal(3,1.2,600)])
axes[2].hist(veri_bi, bins=40, density=True, color='#5B7FA6', alpha=0.5, edgecolor='white')
kde = stats.gaussian_kde(veri_bi, bw_method='silverman')
x_k = np.linspace(-6, 7, 300)
axes[2].plot(x_k, kde(x_k), 'r-', lw=2.5, label='KDE (Silverman)')
axes[2].set_title('Bimodal Dağılım + KDE', fontweight='bold')
axes[2].legend(fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "histogram.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── C. Kutu Grafiği: Tukey Beş Sayı Özeti ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

gruplar = ['A','B','C','D','E']
veriler = [
    np.random.normal(50, 8,  80),
    np.random.normal(60, 12, 80),
    np.concatenate([np.random.normal(40,5,60), np.array([85,88,90])]),
    np.random.normal(55, 6,  80),
    np.random.normal(70, 15, 80),
]

bp = axes[0].boxplot(veriler, labels=gruplar, patch_artist=True,
                     medianprops={'color':'red','lw':2},
                     flierprops={'marker':'o','markerfacecolor':'red','markersize':5})
for patch, c in zip(bp['boxes'], plt.cm.Blues(np.linspace(0.3,0.8,5))):
    patch.set_facecolor(c); patch.set_alpha(0.7)
axes[0].set_title('Tukey Kutu Grafiği\n(Q1-Medyan-Q3 + IQR bıyıkları)', fontweight='bold')
axes[0].grid(axis='y', alpha=0.4)

vp = axes[1].violinplot(veriler, positions=range(1,6), showmedians=True)
for pc in vp['bodies']:
    pc.set_facecolor('#2E5F8A'); pc.set_alpha(0.5)
axes[1].boxplot(veriler, positions=range(1,6), widths=0.1, patch_artist=True,
                boxprops={'facecolor':'white'}, medianprops={'color':'red','lw':2})
axes[1].set_xticks(range(1,6)); axes[1].set_xticklabels(gruplar)
axes[1].set_title('Violin + Box Kombinasyonu', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "kutu.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── D. Dağılım Grafiği: Pearson r ───────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Korelasyon Yapıları (Pearson r)', fontsize=14, fontweight='bold')

for ax, (baslik, hedef_r, tip) in zip(axes.flat, [
    ('Güçlü Pozitif (r≈0.95)',  0.95, 'lin'),
    ('Güçlü Negatif (r≈-0.90)', -0.90, 'lin'),
    ('Zayıf (r≈0.30)',           0.30, 'lin'),
    ('Doğrusal Olmayan',          0.0, 'kare'),
]):
    n2 = 150
    x2 = np.random.randn(n2)
    if tip == 'lin':
        gst = np.sqrt(max(1 - hedef_r**2, 0.01)) / max(abs(hedef_r), 0.1)
        y2 = hedef_r * x2 + gst * np.random.randn(n2)
    else:
        x2 = np.linspace(-3,3,n2); y2 = x2**2 + np.random.randn(n2)*0.5
    r = np.corrcoef(x2, y2)[0,1]
    ax.scatter(x2, y2, alpha=0.6, c=y2, cmap='coolwarm', s=25, edgecolors='none')
    m, b = np.polyfit(x2, y2, 1)
    xf = np.linspace(x2.min(), x2.max(), 100)
    ax.plot(xf, m*xf+b, 'k-', lw=2, alpha=0.8)
    ax.set_title(f'{baslik}\nr = {r:.3f}', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "dagilim.png"), dpi=120, bbox_inches='tight'); plt.close()
print("Tüm temel grafik türleri oluşturuldu.")
