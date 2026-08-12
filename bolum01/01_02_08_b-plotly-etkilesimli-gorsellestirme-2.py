# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.8. Görselleştirme Kütüphaneleri: seaborn ve Plotly › B. Plotly — Etkileşimli Görselleştirme
# Kitap  : Kod 1.57 (Jupyter'da: fig.show()) · Kod 1.58 (Jupyter'da: fig.show())
# Dosya : bolum01/01_02_08_b-plotly-etkilesimli-gorsellestirme-2.py
# Gerekli: pip install pandas plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd, numpy as np

# Basit etkileşimli scatter
np.random.seed(42)
df = pd.DataFrame({
    'gelir'  : np.abs(np.random.normal(55000, 20000, 200)),
    'mutluluk': np.random.uniform(1, 10, 200),
    'sehir'  : np.random.choice(['Istanbul','Ankara','Izmir','Bursa'], 200),
    'yas'    : np.random.randint(20, 65, 200),
})

fig = px.scatter(df, x='gelir', y='mutluluk', color='sehir', size='yas',
                 hover_data=['yas'], title='Gelir–Mutluluk İlişkisi',
                 labels={'gelir':'Yıllık Gelir (TL)', 'mutluluk':'Mutluluk Skoru'})
# Jupyter'da: fig.show()
# HTML olarak kaydet: fig.write_html("grafik.html")
print("Plotly grafiği oluşturuldu (fig.show() ile görüntüleyebilirsiniz)")
