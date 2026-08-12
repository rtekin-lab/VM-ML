# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.6. Bozuk Veri Tespit Yöntemleri › 3.1.6.3. Görselleştirme Teknikleri
# Kitap  : Kod 3.12 (Çok panelli görsel kalite raporu)
# Dosya : bolum03/03_01_06_03_gorsellestirme-teknikleri.py
# Gerekli: pip install matplotlib numpy pandas scipy seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Cok panelli gorsel kalite raporu ───────────────────────────
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(7)
df_vis = pd.DataFrame({
    "gelir":   np.concatenate([np.random.lognormal(8.5,0.7,300),[500000,-1000]]),
    "yas":     np.concatenate([np.random.normal(40,12,300),[150,-5]]),
    "harcama": np.concatenate([np.random.normal(3000,800,300),[50000,-200]]),
})

renkler = ["#2196F3","#FF5722","#4CAF50"]
fig = plt.figure(figsize=(16, 12))
gs  = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35)

for i, col in enumerate(df_vis.columns):
    # Histogram + KDE
    ax_h = fig.add_subplot(gs[i, 0])
    sns.histplot(df_vis[col], bins=35, kde=True, ax=ax_h, color=renkler[i])
    ax_h.set_title(f"{col} - Histogram", fontsize=10)

    # Kutu grafigi
    ax_b = fig.add_subplot(gs[i, 1])
    sns.boxplot(y=df_vis[col], ax=ax_b, color=renkler[i])
    ax_b.set_title(f"{col} - Kutu Grafigi", fontsize=10)

    # Q-Q grafigi
    ax_q = fig.add_subplot(gs[i, 2])
    stats.probplot(df_vis[col].dropna(), dist="norm", plot=ax_q)
    ax_q.set_title(f"{col} - Q-Q Grafigi", fontsize=10)

plt.suptitle("Cok Degiskenli Veri Kalite Gorsel Raporu", fontsize=14, fontweight="bold")
plt.savefig("veri_kalite_raporu.png", dpi=150, bbox_inches="tight")
plt.show()
