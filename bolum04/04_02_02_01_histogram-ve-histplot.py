# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.2. Dagılım Grafikleri: Tek Degiskenli Analiz › 4.2.2.1. Histogram ve histplot
# Kitap  : Kod 4.5 (histplot parametreleri: KDE, normalizasyon, )
# Dosya : bolum04/04_02_02_01_histogram-ve-histplot.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Temel histogram
sns.histplot(data=tips, x="total_bill", ax=axes[0,0],
             color="#3498db", edgecolor="white")
axes[0,0].set_title("Temel Histogram")
axes[0,0].set_xlabel("Toplam Hesap (USD)")

# 2. KDE egri eklenmis histogram
sns.histplot(data=tips, x="total_bill", kde=True, ax=axes[0,1],
             color="#2ecc71", edgecolor="white")
axes[0,1].set_title("Histogram + KDE Egrisi")

# 3. Frekans yerine yogunluk (stat="density")
sns.histplot(data=tips, x="total_bill", stat="density",
             ax=axes[0,2], color="#e74c3c", edgecolor="white")
axes[0,2].set_title("Yogunluk Normlestirilmis")

# 4. Kategoriye gore renklendirme (hue)
sns.histplot(data=tips, x="total_bill", hue="sex",
             ax=axes[1,0], multiple="dodge", shrink=0.8)
axes[1,0].set_title("Cinsiyete Gore (multiple=dodge)")

# 5. Katmanli histogram
sns.histplot(data=tips, x="total_bill", hue="time",
             ax=axes[1,1], multiple="stack", alpha=0.7)
axes[1,1].set_title("Ogune Gore Katmanli")

# 6. 2D histogram (iki degisken)
sns.histplot(data=penguins.dropna(), x="bill_length_mm", y="flipper_length_mm",
             ax=axes[1,2], cbar=True, cmap="Blues")
axes[1,2].set_title("2B Histogram (Isı Haritası)")

plt.suptitle("histplot: Tum Parametreler", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("histplot_ozet.png", dpi=150)
plt.show()
