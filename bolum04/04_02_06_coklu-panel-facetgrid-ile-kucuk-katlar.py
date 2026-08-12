# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.6. Coklu Panel: FacetGrid ile Kucuk Katlar (Small Multiples)
# Kitap  : Kod 4.16 (FacetGrid ile küçük katlar oluşturma)
# Dosya : bolum04/04_02_06_coklu-panel-facetgrid-ile-kucuk-katlar.py
# Gerekli: pip install matplotlib numpy seaborn
# ==========================================================================
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()

# 1. FacetGrid — elle yapılandırma
g = sns.FacetGrid(data=tips, col="time", row="smoker",
                  height=4, aspect=1.2,
                  margin_titles=True)

# map_dataframe ile ozel cizim fonksiyonu
g.map_dataframe(sns.histplot, x="total_bill", kde=True,
                color="#3498db", edgecolor="white")

g.set_axis_labels("Toplam Hesap (USD)", "Sayi")
g.set_titles(row_template="{row_name}", col_template="{col_name}")
g.add_legend()
g.fig.suptitle("FacetGrid: Ogun x Sigara Durumuna Gore Dagilim",
               y=1.02, fontweight="bold")
plt.show()

# 2. FacetGrid ile coklu cizim katmani
g2 = sns.FacetGrid(data=penguins, col="island",
                   hue="species", height=4, aspect=1.1,
                   palette="Set1")
g2.map(sns.scatterplot, "bill_length_mm", "body_mass_g", alpha=0.6, s=40)
g2.map(sns.regplot, "bill_length_mm", "body_mass_g",
       scatter=False, ci=None)
g2.add_legend(title="Tur")
g2.set_axis_labels("Bur Uzunlugu (mm)", "Vucut Agirligi (g)")
g2.set_titles("{col_name} Adasi")
plt.show()

# 3. displot ile facet
g3 = sns.displot(data=tips, x="total_bill", col="day",
                 hue="sex", kind="kde", fill=True,
                 col_wrap=2, height=4, aspect=1.3,
                 palette="Set2",
                 col_order=["Thur","Fri","Sat","Sun"])
g3.set_titles("{col_name}")
plt.show()
