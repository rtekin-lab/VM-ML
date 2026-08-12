# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.8. Kapsamli Ornek: Uctan Uca Kesfedici Veri Analizi (EDA) Panosu
# Kitap  : Kod 4.19 (Titanic veri setinde dokuz panelli keşifsel )
# Dosya : bolum04/04_02_08_kapsamli-ornek-uctan-uca-kesfedici-veri-analizi.py
# Gerekli: pip install matplotlib numpy pandas seaborn
# ==========================================================================
# ─── Titanic EDA Panosu: Seaborn Kapsamli Ornek ─────────────────
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)

titanic = sns.load_dataset("titanic")
print("Eksik deger:")
print(titanic.isnull().sum()[titanic.isnull().sum()>0])

# Temizleme
df = titanic.dropna(subset=["age","embarked","embark_town"]).copy()
df["age_grubu"] = pd.cut(df["age"], bins=[0,18,35,60,100],
                          labels=["Cocuk","Genc","Orta","Yasli"])

fig = plt.figure(figsize=(20, 20))

# ─── Panel 1: Yas Dagılimi (KDE + rug) ───────────────────────────
ax1 = fig.add_subplot(4, 3, 1)
sns.kdeplot(data=df, x="age", hue="survived",
            fill=True, alpha=0.4, ax=ax1, palette="Set1")
ax1.set_title("Hayatta Kalma - Yas Dagılimi")

# ─── Panel 2: Sinif x Cinsiyet Hayatta Kalma Orani ──────────────
ax2 = fig.add_subplot(4, 3, 2)
ozet = df.groupby(["pclass","sex"])["survived"].mean().reset_index()
sns.barplot(data=ozet, x="pclass", y="survived", hue="sex",
            ax=ax2, palette="Set2", capsize=0.1)
ax2.set_ylabel("Hayatta Kalma Orani")
ax2.set_title("Sinif x Cinsiyet")
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y,_: f"%{y*100:.0f}"))

# ─── Panel 3: Bilet Ucreti Violin ────────────────────────────────
ax3 = fig.add_subplot(4, 3, 3)
sns.violinplot(data=df, x="pclass", y="fare", hue="survived",
               split=True, inner="quart", ax=ax3, palette="husl")
ax3.set_yscale("log")
ax3.set_title("Bilet Ucreti (Log) — Sinif Bazli")

# ─── Panel 4: Yolcu Sinifi Sayimi ───────────────────────────────
ax4 = fig.add_subplot(4, 3, 4)
sns.countplot(data=df, x="pclass", hue="survived", ax=ax4,
              palette="Set1")
ax4.set_title("Sinif Dagılimi ve Hayatta Kalma")

# ─── Panel 5: Ambar Liman x Hayatta Kalma ────────────────────────
ax5 = fig.add_subplot(4, 3, 5)
sns.boxplot(data=df, x="embark_town", y="fare", hue="survived",
            ax=ax5, palette="coolwarm")
ax5.set_title("Liman ve Ucret — Hayatta Kalma")
ax5.tick_params(axis="x", rotation=10)

# ─── Panel 6: Yas Grubu x Sinif Heatmap ─────────────────────────
ax6 = fig.add_subplot(4, 3, 6)
pivot = df.pivot_table(index="age_grubu", columns="pclass",
                        values="survived", aggfunc="mean")
sns.heatmap(pivot, annot=True, fmt=".0%", cmap="RdYlGn",
            vmin=0, vmax=1, ax=ax6, linewidths=0.5)
ax6.set_title("Yas Grubu x Sinif: Hayatta Kalma Orani")

# ─── Panel 7: Yas x Ucret Sacilim ───────────────────────────────
ax7 = fig.add_subplot(4, 3, 7)
sns.scatterplot(data=df, x="age", y="fare", hue="survived",
                style="sex", size="pclass", sizes=(30,150),
                ax=ax7, alpha=0.6, palette="Set1")
ax7.set_yscale("log")
ax7.set_title("Yas x Ucret (cok degiskenli)")

# ─── Panel 8: Hayatta Kalma Orani — Kardesler ───────────────────
ax8 = fig.add_subplot(4, 3, 8)
ozet2 = df.groupby("sibsp")["survived"].agg(["mean","count"]).reset_index()
ozet2.columns = ["sibsp","oran","sayi"]
sns.barplot(data=ozet2[ozet2["sayi"]>5], x="sibsp", y="oran",
            ax=ax8, color="#3498db", capsize=0.1)
ax8.set_ylabel("Hayatta Kalma Orani")
ax8.set_xlabel("Kardes/Esler Sayisi")
ax8.set_title("Aile Buyuklugu ve Hayatta Kalma")

# ─── Panel 9: Korelasyon Matrisi ─────────────────────────────────
ax9 = fig.add_subplot(4, 3, 9)
sayisal = df[["survived","pclass","age","sibsp","parch","fare"]].corr()
maske = np.triu(np.ones_like(sayisal, dtype=bool))
sns.heatmap(sayisal, ax=ax9, annot=True, fmt=".2f",
            cmap="vlag", center=0, mask=maske, linewidths=0.3)
ax9.set_title("Korelasyon Matrisi")

plt.suptitle("Titanic Veri Seti: Kapsamli EDA Panosu (Seaborn)",
             fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("titanic_eda_panosu.png", dpi=150, bbox_inches="tight")
plt.show()
print("EDA panosu kaydedildi.")
