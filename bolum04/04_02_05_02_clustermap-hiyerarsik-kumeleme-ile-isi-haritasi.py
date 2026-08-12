# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.5. Isi Haritalari ve Kume Haritasi: heatmap ve clustermap › 4.2.5.2. clustermap: Hiyerarsik Kumeleme ile Isi Haritasi
# Kitap  : Kod 4.15 (clustermap ile hiyerarşik kümeleme sıralamal)
# Dosya : bolum04/04_02_05_02_clustermap-hiyerarsik-kumeleme-ile-isi-haritasi.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Iris veri seti ile clustermap
iris = sns.load_dataset("iris")
X = iris.drop("species", axis=1)

# Standardize et
Xs = StandardScaler().fit_transform(X)
Xs_df = pd.DataFrame(Xs, columns=X.columns, index=iris["species"])

g = sns.clustermap(
    Xs_df,
    method="ward",      # Linkage yontemi: ward, complete, average, single
    metric="euclidean", # Uzaklik metrigi
    cmap="vlag",        # Renk skalasi
    figsize=(10, 8),
    row_colors=iris["species"].map({
        "setosa":"#e74c3c","versicolor":"#3498db","virginica":"#2ecc71"
    }),
    z_score=None,       # Satirlari z-standartlestir: 0=satir, 1=sutun
    annot=False,
    linewidths=0,
    dendrogram_ratio=(0.2, 0.15)
)
g.fig.suptitle("Clustermap: Iris (Ward Baglantisi, Euclidean)", y=1.01)
plt.show()

# Korelasyon matrisi clustermap
penguins = sns.load_dataset("penguins").dropna()
corr = penguins.select_dtypes("number").corr()

g2 = sns.clustermap(corr, cmap="coolwarm", center=0,
                    vmin=-1, vmax=1, annot=True, fmt=".2f",
                    figsize=(8, 8), method="average")
g2.fig.suptitle("Korelasyon Clustermap (Penguen)", y=1.01)
plt.show()
