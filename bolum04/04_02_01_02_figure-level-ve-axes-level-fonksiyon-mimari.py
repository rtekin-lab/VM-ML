# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.1. Seaborn'a Giris: Mimari ve Kurulum › 4.2.1.2. Figure-Level ve Axes-Level Fonksiyon Mimari
# Kitap  : Kod 4.4 (Figure-level ile axes-level fonksiyonların f)
# Dosya : bolum04/04_02_01_02_figure-level-ve-axes-level-fonksiyon-mimari.py
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum04/04_02_01_01_matplotlib-ile-iliskisi-api-katmanlari.py
import seaborn as sns
tips = sns.load_dataset("tips")     # internet gerektirir
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

import matplotlib.pyplot as plt
import seaborn as sns
# FIGURE-LEVEL ornek: displot kendi Figure'ini olusturur
g = sns.displot(data=tips, x="total_bill", col="time", hue="sex",
                kind="kde", height=4, aspect=1.2)
g.set_axis_labels("Toplam Hesap (USD)", "Yogunluk")
g.set_titles(col_template="{col_name} vakti")
plt.show()

# AXES-LEVEL ornek: mevcut Axes'e ciziyor
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(data=tips, x="total_bill", kde=True, ax=axes[0],
             color="#3498db", edgecolor="white")
axes[0].set_title("Histplot (Axes-Level)")

sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[1],
            palette="Set2")
axes[1].set_title("Boxplot (Axes-Level)")

plt.tight_layout()
plt.show()
