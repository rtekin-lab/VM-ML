# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.3. Kategorik Grafikler: Dagilim ve Kestirim › 4.2.3.3. Cubuk ve Nokta Grafikleri: barplot ve pointplot
# Kitap  : Kod 4.10 (barplot ve pointplot ile kestirim, güven ara)
# Dosya : bolum04/04_02_03_03_cubuk-ve-nokta-grafikleri-barplot-ve-pointplot.py
# Gerekli: pip install matplotlib seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Ortalama ve %95 GA cubuk grafigi
sns.barplot(data=tips, x="day", y="total_bill",
            ax=axes[0,0], palette="Blues_d", capsize=0.1,
            order=["Thur","Fri","Sat","Sun"])
axes[0,0].set_title("Ortalama Toplam Hesap (%95 GA)")

# 2. Hue ile grup karsilastirmasi
sns.barplot(data=tips, x="day", y="total_bill", hue="sex",
            ax=axes[0,1], palette="muted", capsize=0.08,
            order=["Thur","Fri","Sat","Sun"])
axes[0,1].set_title("Gun ve Cinsiyet Etkilesimi")

# 3. pointplot — etkilesim analizi
sns.pointplot(data=tips, x="day", y="tip", hue="smoker",
              ax=axes[1,0], palette="Set1", capsize=0.1,
              linestyles=["-","--"], markers=["o","s"],
              order=["Thur","Fri","Sat","Sun"])
axes[1,0].set_title("Etkilesim: Gun x Sigara Durum")

# 4. Titanic hayatta kalma orani
sns.barplot(data=titanic, x="pclass", y="survived",
            hue="sex", ax=axes[1,1],
            palette={"male":"#3498db","female":"#e91e63"},
            capsize=0.1)
axes[1,1].set_title("Titanic: Sinif ve Cinsiyet Hayatta Kalma Orani")
axes[1,1].set_ylabel("Hayatta Kalma Orani")

plt.suptitle("barplot ve pointplot: Kestirim Grafikleri", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
