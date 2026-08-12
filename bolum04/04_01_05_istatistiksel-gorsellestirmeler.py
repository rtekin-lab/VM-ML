# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.5. İstatistiksel Görselleştirmeler
# Kitap  : Kod 4.1 (İstatistiksel grafikler: hata çubuğu ve kore)
# Dosya : bolum04/04_01_05_istatistiksel-gorsellestirmeler.py
# Gerekli: pip install matplotlib numpy pandas scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd

np.random.seed(42)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ─── Hata Çubukları: CI = x̄ ± 1.96×SE ────────────────────────────────────────
n_g = 6; gruplar = [f'Grup {i}' for i in range(1,n_g+1)]
ort = np.random.uniform(40, 80, n_g)
std = np.random.uniform(3, 12, n_g)
ns  = np.random.randint(20, 80, n_g)
SE  = std / np.sqrt(ns)      # Standart Hata
CI  = 1.96 * SE              # %95 Güven Aralığı

x_pos = np.arange(n_g)
axes[0].bar(x_pos, ort, yerr=CI, color='#2E5F8A', alpha=0.75, capsize=6,
            error_kw={'linewidth':1.5,'capthick':1.5}, edgecolor='white', width=0.6)
for i,(mu,se,n) in enumerate(zip(ort,SE,ns)):
    y_j = np.random.normal(mu, se*2, min(n,20))
    axes[0].scatter(np.full_like(y_j,x_pos[i])+np.random.uniform(-0.2,0.2,len(y_j)),
                    y_j, alpha=0.4, s=15, color='white', zorder=5)
axes[0].set_xticks(x_pos); axes[0].set_xticklabels(gruplar)
axes[0].set_title('Çubuk + %95 Güven Aralığı\n(CI = x̄ ± 1.96×SE)', fontweight='bold')
axes[0].set_ylabel('Ortalama Değer')

# ─── Korelasyon Matrisi Isı Haritası ─────────────────────────────────────────
X = pd.DataFrame({
    'Boy(cm)':   np.random.normal(170,10,200),
    'Kilo(kg)':  np.random.normal(70,15,200),
    'Yaş':       np.random.randint(20,60,200).astype(float),
    'Gelir(k₺)': np.random.normal(15,5,200),
    'BMI':       np.random.normal(24,4,200),
})
kor = X.corr()
mask = np.triu(np.ones_like(kor, dtype=bool), k=1)
kor_alt = kor.copy(); kor_alt[mask] = np.nan

im = axes[1].imshow(kor_alt, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=axes[1], shrink=0.85)
for i in range(len(kor)):
    for j in range(len(kor)):
        if not mask[i,j]:
            r = kor_alt.iloc[i,j]
            axes[1].text(j, i, f'{r:.2f}', ha='center', va='center',
                         fontsize=9, fontweight='bold',
                         color='white' if abs(r)>0.5 else 'black')
axes[1].set_xticks(range(len(X.columns)))
axes[1].set_yticks(range(len(X.columns)))
axes[1].set_xticklabels(X.columns, rotation=45, ha='right', fontsize=9)
axes[1].set_yticklabels(X.columns, fontsize=9)
axes[1].set_title('Korelasyon Matrisi (Alt Üçgen)', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "istatistiksel.png"), dpi=120, bbox_inches='tight'); plt.close()
print("İstatistiksel grafikler tamamlandı.")
