# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.2. Figure ve Axes: McKinney'in Önerdiği OOP Yaklaşımı
# Dosya : bolum04/04_01_02_figure-ve-axes-mckinney-in-onerdigi-oop-yaklasim.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# ─── Yöntem 1: plt.subplots() — McKinney önerisi ─────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 2 * np.pi, 300)
ax.plot(x, np.sin(x), label='sin(x)', color='#2E5F8A', linewidth=2)
ax.plot(x, np.cos(x), label='cos(x)', color='#C44D34', linewidth=2, linestyle='--')
ax.set_title('Trigonometrik Fonksiyonlar', fontsize=14, fontweight='bold')
ax.set_xlabel('x (radyan)', fontsize=12)
ax.set_ylabel('f(x)', fontsize=12)
ax.legend(loc='upper right')
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "trig.png"), dpi=120, bbox_inches='tight')
plt.close()

# ─── Yöntem 2: 2×2 Alt Grafik ────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('2×2 Alt Grafik Düzeni', fontsize=16, fontweight='bold')
np.random.seed(42); n = 200

# [0,0] Çizgi
t = np.linspace(0, 4*np.pi, 300)
axes[0,0].plot(t, np.exp(-0.1*t)*np.sin(t), color='#1E3A5F', lw=2)
axes[0,0].fill_between(t, np.exp(-0.1*t)*np.sin(t), alpha=0.2, color='#1E3A5F')
axes[0,0].set_title('Sönümlü Osilatör', fontweight='bold')

# [0,1] Scatter renk kodlamalı
x_s = np.random.randn(n); y_s = 0.8*x_s + np.random.randn(n)*0.5
sc  = axes[0,1].scatter(x_s, y_s, c=np.abs(x_s), cmap='viridis', alpha=0.7, s=30)
fig.colorbar(sc, ax=axes[0,1], shrink=0.9)
axes[0,1].set_title('Scatter + Renk Kodlama', fontweight='bold')

# [1,0] Histogram
data = np.concatenate([np.random.normal(-2,1,100), np.random.normal(3,1.5,100)])
axes[1,0].hist(data, bins=30, color='#2E5F8A', edgecolor='white', alpha=0.85)
axes[1,0].axvline(data.mean(), color='red', ls='--', lw=2, label=f'μ={data.mean():.2f}')
axes[1,0].legend(); axes[1,0].set_title('İkimotlu Histogram', fontweight='bold')

# [1,1] Çubuk
kat = ['A','B','C','D','E']; deg = [23,45,12,67,34]
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(kat)))
bars = axes[1,1].bar(kat, deg, color=colors, edgecolor='white')
for bar,val in zip(bars,deg):
    axes[1,1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                   str(val), ha='center', fontweight='bold')
axes[1,1].set_title('Etiketli Çubuk', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "subplots.png"), dpi=120, bbox_inches='tight')
plt.close()

# ─── Yöntem 3: GridSpec — Asimetrik Düzen ─────────────────────────────────────
fig = plt.figure(figsize=(12, 7))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

ax_main = fig.add_subplot(gs[:, 0:2])   # sol büyük panel
ax_top  = fig.add_subplot(gs[0, 2])     # sağ üst
ax_bot  = fig.add_subplot(gs[1, 2])     # sağ alt

x = np.linspace(0,10,500); y = np.sin(x)*np.exp(-0.1*x)
ax_main.plot(x, y, lw=2, color='#1E3A5F')
ax_main.fill_between(x, y, where=(y>0), alpha=0.3, color='green', label='Pozitif')
ax_main.fill_between(x, y, where=(y<0), alpha=0.3, color='red',   label='Negatif')
ax_main.legend(); ax_main.set_title('GridSpec: Ana Panel (2×2)', fontweight='bold')

ax_top.hist(np.random.exponential(1.5,500), bins=25, color='#C44D34', alpha=0.8)
ax_top.set_title('Üstel Dağılım')
theta = np.linspace(0, 2*np.pi, 200)
ax_bot.plot(np.cos(theta), np.sin(theta), '#2E5F8A', lw=2)
ax_bot.set_aspect('equal'); ax_bot.set_title('Birim Çember')

plt.savefig(os.path.join(tempfile.gettempdir(), "gridspec.png"), dpi=120, bbox_inches='tight')
plt.close()
print("Tüm düzenler kaydedildi.")
