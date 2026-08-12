# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.2. API'ler ve API Entegrasyonları › Kimlik Doğrulama ve Yetkilendirme Mekanizmaları
# Kitap  : Kod 2.18 (REST API kimlik doğrulama: API anahtarı ve O)
# Dosya : bolum02/02_03_02_kimlik-dogrulama-ve-yetkilendirme-mekanizmalari.py
# Gerekli: pip install pandas requests
# ==========================================================================
import requests
import time
import os
import pandas as pd

class HavaAPIIstemcisi:
    """
    OpenWeatherMap API entegrasyonu için yapılandırılmış istemci sınıfı.
    Özellikler: Otomatik hata yönetimi, üstel geri çekilme (exponential backoff).
    """
    def __init__(self, api_anahtari):
        self.api_anahtari = api_anahtari
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
        self._cache = {} # Basit bellek içi önbellekleme

    def _istek_gonder(self, endpoint, params, max_deneme=3):
        url = f"{self.base_url}/{endpoint}"
        params.update({'appid': self.api_anahtari, 'units': 'metric', 'lang': 'tr'})

        for deneme in range(max_deneme):
            try:
                # Simülasyon gereği burada statik bir yanit dondurulmustur.
                # Gerçek kullanım: response = self.session.get(url, params=params)
                print(f"[İstek] {endpoint} | Deneme: {deneme + 1}")
                return {"main": {"temp": 20.5}, "name": params.get("q"), "weather": [{"description": "açık"}]}

            except requests.exceptions.RequestException as e:
                bekleme = 2 ** deneme # Üstel geri çekilme stratejisi
                print(f"Hata: {e}. {bekleme} sn bekleniyor...")
                time.sleep(bekleme)
        return None

    def anlik_hava(self, sehir):
        if sehir in self._cache:
            return self._cache[sehir]

        veri = self._istek_gonder("weather", {"q": sehir})
        if veri:
            self._cache[sehir] = veri
        return veri

# Uygulama ve Veri Çerçevesi (DataFrame) Oluşturma
API_KEY = os.environ.get('WEATHER_API_KEY', 'demo_key')
istemci = HavaAPIIstemcisi(API_KEY)

sehirler = ["Istanbul", "Ankara"]
sonuclar = [istemci.anlik_hava(s) for s in sehirler]

df_hava = pd.DataFrame([
    {'Şehir': v['name'], 'Sıcaklık': v['main']['temp'], 'Durum': v['weather'][0]['description']}
    for v in sonuclar if v
])
print("\n--- Toplanan Hava Durumu Verileri ---")
print(df_hava)
