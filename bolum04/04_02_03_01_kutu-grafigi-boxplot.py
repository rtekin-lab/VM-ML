# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.3. Kategorik Grafikler: Dagilim ve Kestirim › 4.2.3.1. Kutu Grafigi: boxplot
# Kitap  : Kod 4.8 (Boxplot: gruplu, çentikli ve ham veri noktal)
# Dosya : bolum04/04_02_03_01_kutu-grafigi-boxplot.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Temel boxplot
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0,0],
            palette="Set2", order=["Thur","Fri","Sat","Sun"])
axes[0,0].set_title("Gune Gore Toplam Hesap")

# 2. Hue ile kategorik karsilastirma
sns.boxplot(data=tips, x="day", y="total_bill", hue="sex",
            ax=axes[0,1], palette="husl",
            order=["Thur","Fri","Sat","Sun"])
axes[0,1].set_title("Gun x Cinsiyet Etkilesimi")

# 3. Notch ile guven araligi
sns.boxplot(data=penguins, x="species", y="body_mass_g",
            notch=True, ax=axes[1,0], palette="pastel")
axes[1,0].set_title("Notched Boxplot (Medyan %95 GA)")
axes[1,0].set_ylabel("Vucut Agirligi (g)")

# 4. Yatay boxplot + stripplot
sns.boxplot(data=tips, y="day", x="tip", ax=axes[1,1],
            palette="muted", order=["Thur","Fri","Sat","Sun"])
sns.stripplot(data=tips, y="day", x="tip", ax=axes[1,1],
              color=".25", size=3, alpha=0.5,
              order=["Thur","Fri","Sat","Sun"])
axes[1,1].set_title("Boxplot + Ham Veri Noktasi")

plt.suptitle("boxplot: Kategorik Dagilim Analizi", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
