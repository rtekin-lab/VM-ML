# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.4. Iliski Grafikleri: Cok Degiskenli Analiz › 4.2.4.2. Sacikim Matrisi: pairplot ve PairGrid
# Kitap  : Kod 4.12 (pairplot ve PairGrid ile saçılım matrisi)
# Dosya : bolum04/04_02_04_02_sacikim-matrisi-pairplot-ve-pairgrid.py
# Gerekli: pip install matplotlib seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")
penguins = sns.load_dataset("penguins").dropna()

# 1. Temel pairplot
g1 = sns.pairplot(data=iris, hue="species",
                  palette="Set1",
                  diag_kind="kde",   # Kosegen: KDE
                  plot_kws={"alpha": 0.6, "s": 40})
g1.fig.suptitle("Iris: Pairplot (KDE Kosegen)", y=1.02, fontweight="bold")
plt.show()

# 2. PairGrid ile tam ozellestirme
g2 = sns.PairGrid(data=penguins.drop(columns=["year"]),
                  hue="species", palette="Set2")

# Ust ucgen: KDE egrisi
g2.map_upper(sns.kdeplot, levels=3, warn_singular=False)

# Alt ucgen: sacilim
g2.map_lower(sns.scatterplot, alpha=0.5, s=30)

# Kosegen: histogram
g2.map_diag(sns.histplot, kde=True, alpha=0.5)

g2.add_legend()
g2.fig.suptitle("PairGrid: Ust=KDE, Alt=Scatter, Kosegen=Hist", y=1.02)
plt.show()
