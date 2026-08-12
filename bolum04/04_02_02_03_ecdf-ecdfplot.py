# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.2. Dagılım Grafikleri: Tek Degiskenli Analiz › 4.2.2.3. ECDF: ecdfplot
# Kitap  : Kod 4.7 (ecdfplot ile ampirik birikimli dağılım karşı)
# Dosya : bolum04/04_02_02_03_ecdf-ecdfplot.py
# Gerekli: pip install matplotlib seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax0 = plt.subplots(figsize=(7, 5))   # displot kendi figurunu acar; 2. eksen bos kaliyordu
axes = [ax0]

# ECDF — kategorik karsilastirma
sns.ecdfplot(data=tips, x="total_bill", hue="sex", ax=axes[0])
axes[0].set_title("ECDF: Cinsiyete Gore Toplam Hesap")
axes[0].set_xlabel("Toplam Hesap (USD)")
axes[0].set_ylabel("Kumulatif Olasilik")
axes[0].axhline(0.5, color="gray", linestyle="--", alpha=0.5, label="Medyan")
axes[0].legend()

# displot: hist + kde + rug + ecdf karsilastirma
g = sns.displot(data=tips, x="total_bill", hue="time",
                kind="ecdf", height=5, aspect=1.3)
g.set_axis_labels("Toplam Hesap", "Kumulatif Oran")
g.set_titles("ECDF: Ogun Bazli Karsilastirma")
plt.show()
