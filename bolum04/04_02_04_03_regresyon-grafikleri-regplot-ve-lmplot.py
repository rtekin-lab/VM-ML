# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.4. Iliski Grafikleri: Cok Degiskenli Analiz › 4.2.4.3. Regresyon Grafikleri: regplot ve lmplot
# Kitap  : Kod 4.13 (regplot ve lmplot: doğrusal, polinom ve gürb)
# Dosya : bolum04/04_02_04_03_regresyon-grafikleri-regplot-ve-lmplot.py
# Gerekli: pip install matplotlib numpy pandas seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Basit dogrusal regresyon
sns.regplot(data=tips, x="total_bill", y="tip",
            ax=axes[0,0], scatter_kws={"alpha":0.4,"s":20},
            line_kws={"color":"#e74c3c","lw":2})
axes[0,0].set_title("Dogrusal Regresyon: Hesap -> Bahsis")

# 2. Polinomial regresyon (derece=2)
sns.regplot(data=penguins, x="body_mass_g", y="flipper_length_mm",
            ax=axes[0,1], order=2,
            scatter_kws={"alpha":0.4,"s":20,"color":"#3498db"},   # "c" seaborn ile çakışıyor
            line_kws={"color":"#e74c3c"})
axes[0,1].set_title("Polinomial Regresyon (Derece=2)")

# 3. Robust regresyon (aykiri degerlere dayanikli)
np.random.seed(42)
x = np.random.normal(5, 2, 60)
y = 2*x + np.random.normal(0,1,60)
y_aykiri = y.copy()
y_aykiri[:5] += 20  # aykiri degerler ekle

import pandas as pd
df_aykiri = pd.DataFrame({"x":x,"y":y_aykiri})
sns.regplot(data=df_aykiri, x="x", y="y", ax=axes[1,0],
            line_kws={"color":"red","label":"OLS"},
            scatter_kws={"alpha":0.4})
sns.regplot(data=df_aykiri, x="x", y="y", ax=axes[1,0],
            robust=True, line_kws={"color":"green","ls":"--","label":"Robust"},
            scatter=False)
axes[1,0].legend(); axes[1,0].set_title("OLS vs Robust Regresyon")

plt.tight_layout()
plt.show()          # 2x2 figuru once tamamla (plt.close() onu yok ediyordu)

# 4. lmplot — kendi figurunu olusturur, ax parametresi almaz
g = sns.lmplot(data=tips, x="total_bill", y="tip",
               hue="smoker", col="time",
               height=5, aspect=1.1,
               scatter_kws={"alpha":0.4,"s":25},
               line_kws={"lw":2})
g.set_axis_labels("Toplam Hesap", "Bahsis")
g.set_titles("{col_name} Vakti")
plt.show()
