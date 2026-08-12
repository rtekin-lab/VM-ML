# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.2. Dagılım Grafikleri: Tek Degiskenli Analiz › 4.2.2.2. Cekirdek Yogunluk Tahmini: kdeplot
# Kitap  : Kod 4.6 (Kdeplot: bant genişliği etkisi, iki boyutlu )
# Dosya : bolum04/04_02_02_02_cekirdek-yogunluk-tahmini-kdeplot.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Temel KDE
sns.kdeplot(data=tips, x="total_bill", ax=axes[0,0],
            color="#2E75B6", fill=True, alpha=0.4)
axes[0,0].set_title("Temel KDE")

# 2. Bant genisligi etkisi
for bw, renk, etiket in [(0.2, "#e74c3c", "Dar (bw=0.2)"),
                          (1.0, "#2ecc71", "Normal (bw=1.0)"),
                          (3.0, "#9b59b6", "Genis (bw=3.0)")]  :
    sns.kdeplot(data=tips, x="total_bill", ax=axes[0,1],
                bw_adjust=bw, color=renk, label=etiket)
axes[0,1].set_title("Bant Genisligi (bw_adjust) Etkisi")
axes[0,1].legend(fontsize=8)

# 3. Kategoriye gore KDE
sns.kdeplot(data=tips, x="total_bill", hue="day",
            ax=axes[0,2], fill=True, alpha=0.3)
axes[0,2].set_title("Gune Gore KDE")

# 4. 2D KDE (bivariate)
sns.kdeplot(data=penguins, x="bill_length_mm", y="bill_depth_mm",
            hue="species", ax=axes[1,0], fill=False)
axes[1,0].set_title("2B KDE (bur olculeri, tür bazli)")

# 5. 2D KDE dolgu ile
sns.kdeplot(data=penguins, x="flipper_length_mm", y="body_mass_g",
            ax=axes[1,1], fill=True, levels=8, cmap="viridis")
axes[1,1].set_title("2B KDE (isi haritasi benzeri)")

# 6. Kumulatif KDE
sns.kdeplot(data=tips, x="total_bill", ax=axes[1,2],
            cumulative=True, color="#e67e22")
axes[1,2].set_title("Kumulatif KDE")
axes[1,2].set_ylabel("Kumulatif Olasilik")

plt.suptitle("kdeplot: Tek ve Cift Degiskenli KDE", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
