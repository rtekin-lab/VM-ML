# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.1. Veri Toplama Yöntemleri › Web Kazıma (Web Scraping)
# Kitap  : Kod 2.17 (Hız sınırlamasına saygılı web kazıma döngüsü)
# Dosya : bolum02/02_03_01_web-kazima.py
# Gerekli: pip install beautifulsoup4 pandas requests
# ==========================================================================
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Simüle Edilmiş HTML Modeli (DOM Ağacı)
html_content = """
<!DOCTYPE html>
<html>
<body>
  <div class="haber-listesi">
    <article class="haber" id="h1">
      <h2 class="baslik">Yapay Zeka Arastirmalarinda Yeni Gelismeler</h2>
      <span class="tarih">2024-11-15</span>
      <p class="ozet">Derin ogrenme modelleri yeni bir rekoru kirdi.</p>
    </article>
    <article class="haber" id="h2">
      <h2 class="baslik">Kuantum Hesaplamada Ilerleme</h2>
      <span class="tarih">2024-11-14</span>
      <p class="ozet">Arastirmacilar 1000-kubit barikatini asmayi basardi.</p>
    </article>
  </div>
</body>
</html>
"""

# 2. HTML Ayrıştırma (Parsing)
soup = BeautifulSoup(html_content, 'html.parser')

# 3. Öğe Seçimi ve Yapılandırma
haber_listesi = []
for makale in soup.find_all('article', class_='haber'):
    veri = {
        'id'     : makale.get('id', ''),
        'baslik' : makale.find('h2', class_='baslik').get_text(strip=True),
        'tarih'  : makale.find('span', class_='tarih').get_text(strip=True),
        'ozet'   : makale.find('p', class_='ozet').get_text(strip=True)
    }
    haber_listesi.append(veri)

# 4. pandas Entegrasyonu ve Veri Zenginleştirme
df = pd.DataFrame(haber_listesi)
df['tarih'] = pd.to_datetime(df['tarih'])
df['ozet_kelime_sayisi'] = df['ozet'].str.split().str.len()

print("--- Kazınmış ve Temizlenmiş Veri Seti ---")
print(df[['baslik', 'tarih', 'ozet_kelime_sayisi']])
