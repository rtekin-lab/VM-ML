# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.4. Veri Toplama Sürecinde Karşılaşılan Zorluklar ve Çözüm Stratejileri › Zamanlanmış Görevler ve Akıllı Önbellekleme
# Dosya : bolum02/02_03_04_zamanlanmis-gorevler-ve-akilli-onbellekleme.py
# ==========================================================================
from apscheduler.schedulers.blocking import BlockingScheduler
import time

# 1. Önbellek Yapılandırması (Simüle Edilmiş)
onbellek = {
    'veri': None,
    'son_guncelleme': 0,
    'ttl': 3600  # 1 saatlik yaşam süresi
}

def veri_topla():
    simdi = time.time()

    # TTL Kontrolü: Veri hala güncel mi?
    if onbellek['veri'] and (simdi - onbellek['son_guncelleme'] < onbellek['ttl']):
        print("[Önbellek] Güncel veri mevcut, API isteği atlanıyor.")
        return onbellek['veri']

    # Veri Toplama İşlemi (Simüle)
    print(f"[İşlem] {time.ctime()} itibarıyla yeni veri API'den çekiliyor...")
    onbellek['veri'] = {"deger": "Yeni Veri Seti"}
    onbellek['son_guncelleme'] = simdi
    return onbellek['veri']

# 2. Zamanlayıcı Kurulumu
scheduler = BlockingScheduler()
# Görevi her saat başı çalışacak şekilde programla
scheduler.add_job(veri_topla, 'interval', hours=1)

print("--- Veri Toplama Otomasyonu Başlatıldı ---")
# Not: Eğitim amaçlı ilk çalıştırma manuel tetiklenir
veri_topla()
# scheduler.start() # Gerçek ortamda zamanlayıcıyı başlatır
