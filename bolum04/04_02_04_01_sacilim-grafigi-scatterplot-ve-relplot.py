# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.4. Iliski Grafikleri: Cok Degiskenli Analiz › 4.2.4.1. Sacilim Grafigi: scatterplot ve relplot
# Kitap  : Kod 4.11 (scatterplot ve relplot ile çok değişkenli sa)
# Dosya : bolum04/04_02_04_01_sacilim-grafigi-scatterplot-ve-relplot.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

penguins = sns.load_dataset("penguins").dropna()
tips = sns.load_dataset("tips")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Temel sacilim
sns.scatterplot(data=penguins, x="bill_length_mm", y="flipper_length_mm",
                hue="species", ax=axes[0,0], s=60, alpha=0.8)
axes[0,0].set_title("Tur Bazli Penguen Bur-Kanat Iliskisi")

# 2. Boyut ve stil ekstra degisken
sns.scatterplot(data=penguins, x="bill_length_mm", y="body_mass_g",
                hue="species", size="flipper_length_mm", style="sex",
                ax=axes[0,1], sizes=(20, 200), alpha=0.7)
axes[0,1].set_title("4 Degiskenli Sacilim (hue+size+style)")

# 3. Jitter ile kategorik+sayisal
sns.stripplot(data=tips, x="day", y="total_bill",
              hue="sex", ax=axes[1,0], dodge=True, jitter=0.2, alpha=0.7)
axes[1,0].set_title("Stripplot: Kategorik + Sayisal")

# 4. Swarmplot — ust uste gelmeyen noktalar
sns.swarmplot(data=penguins, x="species", y="flipper_length_mm",
              hue="sex", ax=axes[1,1], dodge=True)
axes[1,1].set_title("Swarmplot: Cakismasiz Noktalar")

plt.suptitle("Sacilim Grafikleri: scatterplot, strip, swarm", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.show()

# relplot — Figure-level, col/row facet
g = sns.relplot(data=penguins, x="bill_length_mm", y="body_mass_g",
               hue="species", col="island", kind="scatter",
               height=4, aspect=1.0, s=50, alpha=0.7)
g.set_axis_labels("Bur Uzunlugu (mm)", "Vucut Agirligi (g)")
g.set_titles("{col_name} Adasi")
plt.show()
