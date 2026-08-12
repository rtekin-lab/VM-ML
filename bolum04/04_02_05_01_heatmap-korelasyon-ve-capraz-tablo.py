# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.5. Isi Haritalari ve Kume Haritasi: heatmap ve clustermap › 4.2.5.1. heatmap: Korelasyon ve Capraz Tablo
# Kitap  : Kod 4.14 (Heatmap: korelasyon matrisi, hata matrisi ve)
# Dosya : bolum04/04_02_05_01_heatmap-korelasyon-ve-capraz-tablo.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

penguins = sns.load_dataset("penguins").dropna()
flights = sns.load_dataset("flights")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Korelasyon haritasi (maske ile)
sayisal = penguins.select_dtypes(include="number")
corr = sayisal.corr()
maske = np.triu(np.ones_like(corr, dtype=bool))  # Ust ucgen gizle

sns.heatmap(corr, annot=True, fmt=".2f", mask=maske,
            cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            ax=axes[0,0], linewidths=0.5, square=True)
axes[0,0].set_title("Korelasyon Matrisi (Alt Ucgen)")

# 2. Ucus verisi — zaman serisi isi haritasi
pivot = flights.pivot_table(index="month", columns="year", values="passengers")

ay_sirasi = ["Jan","Feb","Mar","Apr","May","Jun",
             "Jul","Aug","Sep","Oct","Nov","Dec"]
pivot = pivot.reindex(ay_sirasi).astype(int)   # pivot_table float doner; fmt="d" icin int'e cevir

sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd",
            ax=axes[0,1], linewidths=0.3)
axes[0,1].set_title("Aylik Ucus Sayisi (1949-1960)")

# 3. Siniflandirma hata matrisi
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_i, y_i = load_iris(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X_i, y_i, test_size=0.3, random_state=42)
rf = RandomForestClassifier(random_state=42).fit(X_tr, y_tr)
cm = confusion_matrix(y_te, rf.predict(X_te))
tur_adi = ["Setosa","Versicolor","Virginica"]

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=tur_adi, yticklabels=tur_adi,
            ax=axes[1,0])
axes[1,0].set_xlabel("Tahmin Edilen")
axes[1,0].set_ylabel("Gercek")
axes[1,0].set_title("Hata Matrisi (Random Forest, Iris)")

# 4. Capraz tablo
titanic = sns.load_dataset("titanic")
capraz = pd.crosstab(titanic["class"], titanic["survived"],
                     normalize="index") * 100
sns.heatmap(capraz, annot=True, fmt=".1f", cmap="RdYlGn",
            ax=axes[1,1], vmin=0, vmax=100)
axes[1,1].set_title("Sinif Bazli Hayatta Kalma Orani (%)")

plt.suptitle("heatmap: Korelasyon, Zaman Serisi, Hata Matrisi", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.show()
