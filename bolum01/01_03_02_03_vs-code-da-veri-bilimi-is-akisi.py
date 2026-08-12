# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.2. Visual Studio Code (VS Code) › 1.3.2.3. VS Code'da Veri Bilimi Is Akisi
# Kitap  : Kod 1.69 (Veri_analizi.py — VS Code Interactive Window)
# Dosya : bolum01/01_03_02_03_vs-code-da-veri-bilimi-is-akisi.py
# Gerekli: pip install matplotlib numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# veri_analizi.py  — VS Code Interactive Window ile calistirilir
# Her # %% blogu ayri bir Jupyter hucresi gibi davranir
# Ctrl+Enter: Mevcut hucreli calistir
# Shift+Enter: Calistir ve sonraki hucrege gec

# %% [markdown]
# ## Veri Yukleme ve On Inceleme
# Bu bolumde pandas ile veri setini yukleyip ilk incelemeleri yapiyoruz.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Veri seti yukle (orneklem)
np.random.seed(42)
df = pd.DataFrame({
    "gelir":  np.random.lognormal(10.5, 0.8, 500),
    "yas":    np.random.randint(22, 65, 500),
    "sektor": np.random.choice(["Teknoloji","Finans","Saglik","Egitim"], 500)
})
print(f"Veri seti boyutu: {df.shape}")
df.head()

# %% [markdown]
# ## Istatistiksel Ozet

# %%
# Temel istatistikler
print("=== Sayisal Ozet ===")
print(df.describe().round(2))
print(f"\nEksik deger: {df.isnull().sum().sum()}")

# %% [markdown]
# ## Gorsellestime

# %%
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

df["gelir"].hist(bins=40, ax=axes[0], color="#3498db", alpha=0.7)
axes[0].set_title("Gelir Dagilimi"); axes[0].set_xlabel("Gelir (TL)")

df.boxplot(column="gelir", by="sektor", ax=axes[1])
axes[1].set_title("Sektore Gore Gelir")
plt.suptitle("")          # pandas'in otomatik "Boxplot grouped by ..." basligini kaldir

axes[2].scatter(df["yas"], df["gelir"], alpha=0.3, c="#e74c3c", s=20)
axes[2].set_xlabel("Yas"); axes[2].set_ylabel("Gelir")
axes[2].set_title("Yas - Gelir Iliskisi")

plt.tight_layout()
plt.show()
