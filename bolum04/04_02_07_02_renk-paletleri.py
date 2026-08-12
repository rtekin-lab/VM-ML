# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.7. Grafik Ozellestirme: Stil, Renk Paletleri ve Tema › 4.2.7.2. Renk Paletleri
# Kitap  : Kod 4.18 (Renk paletleri: nitel, sıralı, ıraksak ve re)
# Dosya : bolum04/04_02_07_02_renk-paletleri.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(3, 3, figsize=(16, 12))

# Nitel paletler
nitel = ["Set1","Set2","husl"]
for i, palet in enumerate(nitel):
    sns.barplot(data=tips, x="day", y="total_bill", hue="sex",
                ax=axes[0,i], palette=palet,
                order=["Thur","Fri","Sat","Sun"], capsize=0.08)
    axes[0,i].set_title(f"Nitel: {palet}")
    axes[0,i].set_xlabel(""); axes[0,i].legend(fontsize=8)

# Siralı paletler
siralı = ["Blues","viridis","YlOrRd"]
for i, palet in enumerate(siralı):
    corr = tips.select_dtypes("number").corr()
    sns.heatmap(corr, ax=axes[1,i], cmap=palet,
                annot=True, fmt=".2f", cbar=False)
    axes[1,i].set_title(f"Siralı: {palet}")

# Irksal paletler
irksal = ["RdBu_r","coolwarm","vlag"]
for i, palet in enumerate(irksal):
    corr = tips.select_dtypes("number").corr()
    sns.heatmap(corr, ax=axes[2,i], cmap=palet, center=0,
                annot=True, fmt=".2f", cbar=False, vmin=-1, vmax=1)
    axes[2,i].set_title(f"Irksal: {palet}")

plt.suptitle("Seaborn Renk Paletleri: Nitel, Siralı, Irksal",
             fontsize=14, fontweight="bold")
plt.tight_layout(); plt.show()

# Renk kordigi dostu palette (CBS, WCAG)
print("Colorblind-safe paletler:")
print(sns.color_palette("colorblind"))
sns.palplot(sns.color_palette("colorblind"))
plt.title("colorblind palette"); plt.show()
