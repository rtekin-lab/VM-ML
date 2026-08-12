# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.7. Grafik Ozellestirme: Stil, Renk Paletleri ve Tema › 4.2.7.1. Stil ve Baglam Ayarlari
# Kitap  : Kod 4.17 (seaborn stil ve bağlam sisteminin tüm seçene)
# Dosya : bolum04/04_02_07_01_stil-ve-baglam-ayarlari.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")

# Seaborn stil secenekleri
# "darkgrid", "whitegrid", "dark", "white", "ticks"
stiller = ["darkgrid","whitegrid","dark","white","ticks"]

fig, axes = plt.subplots(1, len(stiller), figsize=(20, 4))
for ax, stil in zip(axes, stiller):
    with sns.axes_style(stil):
        sns.histplot(data=tips, x="total_bill", ax=ax,
                     color="#3498db", edgecolor="white", kde=True)
    ax.set_title(f"stil: {stil}", fontweight="bold")
    ax.set_xlabel(""); ax.set_ylabel("")
plt.tight_layout(); plt.show()

# Baglam (context): "paper","notebook","talk","poster"
# Yazi boyutu ve cizgi kalinligini ölceklendiriyor
baglamlar = ["paper","notebook","talk","poster"]
fig2, axes2 = plt.subplots(1, len(baglamlar), figsize=(22, 5))
for ax, baglam in zip(axes2, baglamlar):
    with sns.plotting_context(baglam):
        sns.boxplot(data=tips, x="day", y="total_bill",
                    ax=ax, palette="Set2")
    ax.set_title(f"context: {baglam}")
plt.tight_layout(); plt.show()
