# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.2. Seaborn › 4.2.1. Seaborn'a Giris: Mimari ve Kurulum › 4.2.1.1. Matplotlib ile Iliskisi: API Katmanlari
# Kitap  : Kod 4.3 (seaborn kurulumu ve hazır veri setlerine eri)
# Dosya : bolum04/04_02_01_01_matplotlib-ile-iliskisi-api-katmanlari.py
# Gerekli: pip install matplotlib numpy pandas seaborn
# ==========================================================================
# Kurulum
# $ pip install seaborn          # pip ile
# $ conda install seaborn -c conda-forge   # conda ile

# Standart import blogu
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

# Seaborn surumunu kontrol et
print(f"Seaborn: {sns.__version__}")   # >= 0.12 onerilir
print(f"Matplotlib: {mpl.__version__}")
print(f"Pandas: {pd.__version__}")

# Seaborn hazir veri setleri
print("Kullanilabilir veri setleri:", sns.get_dataset_names())

# Ornek veri setleri
tips   = sns.load_dataset("tips")     # Restoran bahsisleri
iris   = sns.load_dataset("iris")     # Iris cicek olculeri
titanic= sns.load_dataset("titanic")  # Titanic yolcuları
penguins=sns.load_dataset("penguins") # Penguen turleri
flights= sns.load_dataset("flights")  # Ucus verileri

print(tips.head(3))
print(f"tips boyutu: {tips.shape}")
