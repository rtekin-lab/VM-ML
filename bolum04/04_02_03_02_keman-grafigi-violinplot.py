# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.3. Kategorik Grafikler: Dagilim ve Kestirim › 4.2.3.2. Keman Grafigi: violinplot
# Kitap  : Kod 4.9 (Violinplot: çeyreklikli, bölünmüş ve swarmpl)
# Dosya : bolum04/04_02_03_02_keman-grafigi-violinplot.py
# Gerekli: pip install matplotlib seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Temel violin
sns.violinplot(data=tips, x="day", y="total_bill",
               ax=axes[0,0], palette="Set1",
               order=["Thur","Fri","Sat","Sun"])
axes[0,0].set_title("Violin Grafigi")

# 2. Inner=quartile: ic yapida ceyrekler
sns.violinplot(data=tips, x="day", y="total_bill",
               inner="quartile", ax=axes[0,1], palette="Pastel1",
               order=["Thur","Fri","Sat","Sun"])
axes[0,1].set_title("inner=quartile")

# 3. Split violin: iki kategori karsilastirmasi
sns.violinplot(data=tips, x="day", y="total_bill", hue="sex",
               split=True, inner="quart", ax=axes[1,0],
               palette={"Male":"#3498db","Female":"#e74c3c"},
               order=["Thur","Fri","Sat","Sun"])
axes[1,0].set_title("Split Violin (Cinsiyet)")

# 4. Violin + Swarm birlesimi
sns.violinplot(data=penguins, x="species", y="flipper_length_mm",
               inner=None, ax=axes[1,1], palette="muted", alpha=0.7)
sns.swarmplot(data=penguins, x="species", y="flipper_length_mm",
              ax=axes[1,1], color="white", size=3, alpha=0.9)
axes[1,1].set_title("Violin + Swarm (Penguen Kanat Uzunlugu)")

plt.suptitle("violinplot: KDE + Dagilim Birlesimi", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
