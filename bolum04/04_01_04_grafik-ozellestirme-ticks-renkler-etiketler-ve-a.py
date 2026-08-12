# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.4. Grafik Özelleştirme: Ticks, Renkler, Etiketler ve Annotasyon
# Dosya : bolum04/04_01_04_grafik-ozellestirme-ticks-renkler-etiketler-ve-a.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

np.random.seed(42)

# ─── A. Tick Format Seçenekleri ───────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Para birimi formatı
gelir = np.cumsum(np.random.normal(1000,200,36))
axes[0,0].plot(np.arange(36), gelir, '#1E3A5F', lw=2)
axes[0,0].yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, p: f'₺{x:,.0f}'))
axes[0,0].xaxis.set_major_locator(ticker.MultipleLocator(6))
axes[0,0].fill_between(range(36), gelir, alpha=0.15, color='#1E3A5F')
axes[0,0].set_title('Para Birimi Tick Formatı')

# Log ölçeği
x = np.logspace(-1, 3, 200)
for exp, col in zip([0.5,1.0,1.5,2.0], ['#1E3A5F','#C44D34','#2E8B57','#8B4513']):
    axes[0,1].loglog(x, x**exp, color=col, lw=2, label=f'x^{exp}')
axes[0,1].set_title('Log-Log Ölçeği')
axes[0,1].legend(fontsize=9)
axes[0,1].grid(True, which='both', alpha=0.3)

# Yüzde formatı
kat = ['Ürün A','Ürün B','Ürün C','Ürün D']
pay = [0.35, 0.28, 0.22, 0.15]
bars = axes[1,0].barh(kat, pay, color=plt.cm.Blues(np.linspace(0.4,0.85,4)))
axes[1,0].xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
for bar, pct in zip(bars, pay):
    axes[1,0].text(pct+0.005, bar.get_y()+bar.get_height()/2,
                   f'{pct:.0%}', va='center', fontweight='bold')
axes[1,0].set_title('Yüzde Formatı')

# Renk haritası gradyanları
cmap_list = [('viridis','Sıralı'), ('RdBu','Ayrışan'), ('tab10','Niteliksel')]
for i, (cmap_ad, tip) in enumerate(cmap_list):
    gradient = np.linspace(0,1,256).reshape(1,-1)
    axes[1,1].imshow(gradient, aspect=8, cmap=cmap_ad,
                     extent=[0,10,i-0.4,i+0.4])
    axes[1,1].text(-0.3, i, f'{tip}:\n{cmap_ad}', va='center', ha='right', fontsize=9)
axes[1,1].set_xlim(-1,10); axes[1,1].set_title('Renk Haritası Örnekleri')
axes[1,1].set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "ticks_renkler.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── B. Annotasyon Teknikleri ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))

x = np.linspace(0, 4*np.pi, 500)
y = np.sin(x) * (1 + 0.3*x)
ax.plot(x, y, '#1E3A5F', lw=2.5, label='f(x) = sin(x)·(1+0.3x)')
ax.fill_between(x, y, where=(y>0), alpha=0.2, color='green')
ax.fill_between(x, y, where=(y<0), alpha=0.2, color='red')
ax.axhline(0, color='k', lw=0.8)

# Ok annotasyonu
max_idx = np.argmax(y)
ax.annotate(
    f'Maksimum\n({x[max_idx]:.2f}, {y[max_idx]:.2f})',
    xy=(x[max_idx], y[max_idx]),
    xytext=(x[max_idx]-2.5, y[max_idx]+0.3),
    fontsize=11, fontweight='bold', color='#1E3A5F',
    arrowprops=dict(arrowstyle='->', color='#1E3A5F', lw=1.8,
                    connectionstyle='arc3,rad=-0.3'),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAF1FB', edgecolor='#1E3A5F')
)
ax.axvline(x=np.pi, color='gray', ls='--', lw=1, alpha=0.7)
ax.text(np.pi+0.1, ax.get_ylim()[0]+0.1, 'π', fontsize=14, color='gray')
ax.set_title('İleri Düzey Annotasyon Teknikleri', fontsize=14, fontweight='bold')
ax.legend(); ax.set_xlim(0, 4*np.pi)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "annotasyon.png"), dpi=120, bbox_inches='tight'); plt.close()
print("Özelleştirme grafikleri tamamlandı.")
