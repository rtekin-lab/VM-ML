# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.9. pandas Entegrasyonu: McKinney'nin Analitik İş Akışı
# Dosya : bolum04/04_01_09_pandas-entegrasyonu-mckinney-nin-analitik-is-aki.py
# Gerekli: pip install matplotlib numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)

# ─── Satış Veri Seti ─────────────────────────────────────────────────────────
tarihler = pd.date_range('2023-01-01', periods=52, freq='W')
urunler  = ['Laptop', 'Tablet', 'Telefon', 'Aksesuar']
satis    = pd.DataFrame(
    np.random.poisson([80,120,200,350], size=(52,4)).astype(float),
    index=tarihler, columns=urunler
)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('pandas + matplotlib: Satış Dashboard', fontsize=14, fontweight='bold')

# [0,0] Çizgi — DataFrame.plot()
satis.plot(ax=axes[0,0], lw=2, alpha=0.85, title='Haftalık Satış Trendi')
axes[0,0].set_xlabel('Tarih'); axes[0,0].set_ylabel('Adet')

# [0,1] Aylık gruplama + yığılmış çubuk
# McKinney (2022) Ch.11: resample() ile zaman serisi yeniden örnekleme
aylik = satis.resample('ME').sum()   # pandas >= 2.2: 'M' yerine 'ME'
aylik.plot(kind='bar', stacked=True, ax=axes[0,1], colormap='Blues',
           title='Aylık Yığılmış Satış')
axes[0,1].set_xticklabels([t.strftime('%b') for t in aylik.index], rotation=45)

# [1,0] Pasta grafiği
toplam = satis.sum()
wedges, texts, autos = axes[1,0].pie(
    toplam, labels=toplam.index,
    autopct=lambda p: f'{p:.1f}%\n({int(p*toplam.sum()/100):,})',
    colors=['#1E3A5F','#2E5F8A','#5B8DB8','#A8C6E8'],
    startangle=90, wedgeprops={'edgecolor':'white','linewidth':2}
)
for a in autos: a.set_fontsize(8)
axes[1,0].set_title('Toplam Satış Payı', fontweight='bold')

# [1,1] Korelasyon ısı haritası
kor = satis.corr()
im  = axes[1,1].imshow(kor, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(im, ax=axes[1,1], shrink=0.85)
for i in range(len(kor)):
    for j in range(len(kor)):
        axes[1,1].text(j, i, f'{kor.iloc[i,j]:.2f}', ha='center', va='center',
                       fontsize=9, fontweight='bold',
                       color='white' if abs(kor.iloc[i,j])>0.6 else 'black')
axes[1,1].set_xticks(range(len(urunler))); axes[1,1].set_yticks(range(len(urunler)))
axes[1,1].set_xticklabels(urunler, rotation=45, fontsize=9)
axes[1,1].set_yticklabels(urunler, fontsize=9)
axes[1,1].set_title('Ürün Korelasyon Matrisi', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "pandas_mpl.png"), dpi=120, bbox_inches='tight'); plt.close()
print("pandas + matplotlib entegrasyon grafiği kaydedildi.")
