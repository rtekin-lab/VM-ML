# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.6. Alt Grafikler: Çift Eksen, İç İçe ve Polar Koordinat
# Dosya : bolum04/04_01_06_alt-grafikler-cift-eksen-ic-ice-ve-polar-koordin.py
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

np.random.seed(42)

# ─── A. Çift Y Ekseni (twinx) ─────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 5))
aylar   = np.arange(1,13)
satislar = np.array([150,180,220,270,310,350,330,290,250,200,170,140])
muster   = np.array([1200,1350,1500,1700,1900,2100,2050,1900,1700,1500,1350,1200])

ax2 = ax1.twinx()   # aynı x eksenini paylaşır
l1, = ax1.plot(aylar, satislar, 'b-o', lw=2, ms=7, label='Satış (k₺)')
ax2.bar(aylar, muster, alpha=0.3, color='orange', width=0.6)
l2, = ax2.plot(aylar, muster, 'r--s', lw=1.5, ms=5, alpha=0.8, label='Müşteri')

ax1.set_xlabel('Ay', fontsize=12)
ax1.set_ylabel('Satış (k₺)', fontsize=12, color='blue')
ax2.set_ylabel('Müşteri Sayısı', fontsize=12, color='red')
ax1.tick_params(axis='y', labelcolor='blue')
ax2.tick_params(axis='y', labelcolor='red')
ax1.set_xticks(aylar)
ax1.set_xticklabels(['Oca','Şub','Mar','Nis','May','Haz',
                      'Tem','Ağu','Eyl','Eki','Kas','Ara'])
ax1.legend([l1,l2], ['Satış','Müşteri'], loc='upper left', fontsize=9)
ax1.set_title('Çift Y Ekseni: Satış ve Müşteri Sayısı', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "cift_eksen.png"), dpi=120); plt.close()

# ─── B. İç İçe (Inset) Grafik ─────────────────────────────────────────────────
fig, ax_main = plt.subplots(figsize=(12, 7))
t = np.linspace(0, 10, 1000)
sinyal = np.sin(2*np.pi*3*t) * np.exp(-0.2*t)
ax_main.plot(t, sinyal, '#1E3A5F', lw=1.5, alpha=0.8)
ax_main.set_title('Sönümlü Sinyal + İç İçe Yakınlaştırma', fontweight='bold', fontsize=13)
ax_main.set_xlabel('Zaman (s)'); ax_main.set_ylabel('Genlik')

# inset_axes: [x, y, genişlik, yükseklik] eksen koordinatlarında
ax_ins = ax_main.inset_axes([0.55, 0.55, 0.42, 0.38])
mask_z = (t >= 0) & (t <= 1.5)
ax_ins.plot(t[mask_z], sinyal[mask_z], '#C44D34', lw=2)
ax_ins.set_title('Yakınlaştırma [0-1.5s]', fontsize=9, fontweight='bold')
ax_ins.set_facecolor('#FFF8F0')
ax_main.indicate_inset_zoom(ax_ins, edgecolor='#C44D34', linewidth=1.5)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "inset.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── C. Polar Koordinatlar: Rüzgar Gülü ve Radar ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection':'polar'})

# Rüzgar gülü diyagramı
yonler = np.deg2rad(np.arange(0, 360, 22.5))
hizlar = np.random.uniform(5, 30, len(yonler))
bars_p = axes[0].bar(yonler, hizlar, width=2*np.pi/len(yonler),
                      color=plt.cm.viridis(hizlar/hizlar.max()), alpha=0.8)
axes[0].set_theta_zero_location('N'); axes[0].set_theta_direction(-1)
axes[0].set_xticks(yonler[::2])
axes[0].set_xticklabels(['K','KD','D','GD','G','GB','B','KB'], fontsize=9)
axes[0].set_title('Rüzgar Gülü Diyagramı', fontsize=11, fontweight='bold')

# Radar grafiği
kat_r = ['Teknik','Analitik','İletişim','Liderlik','Yaratıcılık']
n_c   = len(kat_r)
acilar = np.linspace(0, 2*np.pi, n_c, endpoint=False).tolist() + [0]
ka     = [8,7,6,5,9,8]; kb = [6,9,8,7,5,6]
axes[1].plot(acilar, ka, 'b-o', lw=2, label='Kişi A')
axes[1].fill(acilar, ka, alpha=0.2, color='blue')
axes[1].plot(acilar, kb, 'r-s', lw=2, label='Kişi B')
axes[1].fill(acilar, kb, alpha=0.2, color='red')
axes[1].set_xticks(acilar[:-1])
axes[1].set_xticklabels(kat_r, fontsize=9)
axes[1].set_ylim(0,10)
axes[1].set_title('Radar: Yetkinlik Karşılaştırması', fontsize=11, fontweight='bold')
axes[1].legend(loc='upper right', bbox_to_anchor=(1.3,1.1))

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "polar.png"), dpi=120, bbox_inches='tight'); plt.close()
print("Alt grafik düzenleri tamamlandı.")
