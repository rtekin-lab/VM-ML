# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.3. PyCharm › 1.3.3.2. PyCharm'in Guclu Ozellikleri
# Kitap  : Kod 1.72 (PyCharm özellikleri — profiling ve kod anali)
# Dosya : bolum01/01_03_03_02_pycharm-in-guclu-ozellikleri.py
# ==========================================================================
# ─── 1. Akilli Yeniden Adlandirma (Smart Refactor) ──────────────
# Shift+F6 ile bir sinif, fonksiyon veya degisken adini degistirdiginde
# PyCharm projedeki TUM kullanim yerlerini otomatik gunceller

# ─── 2. Kod Inspections ─────────────────────────────────────────
# PyCharm 400+ kod kalite denetimi yapar:
# - Kullanilmayan import tespiti
# - Tip uyumsuzlugu uyarilari (PEP 484)
# - Sonsuz dongu tespiti
# - Erisim kontrolu ihlalleri

# ─── 3. Database Tools (Pro) ─────────────────────────────────────
# View > Tool Windows > Database
# PostgreSQL, MySQL, SQLite baglantisi
# SQL sorgusu calistir, sonuclari DataFrame'e donustur

# ─── 4. Profiling ────────────────────────────────────────────────
# Run > Profile "dosya.py"
# Satirsal yuzde ve cagri agaci görsellestirilir
# Ornek: Hangi fonksiyon toplam surenin yuzde kacini aliyor?

import cProfile
import pstats
import io

def agir_hesaplama(n=100_000):
    return sum(i**2 for i in range(n))

def hafif_hesaplama(n=100_000):
    return sum(range(n))

def ana():
    for _ in range(10):
        agir_hesaplama()
        hafif_hesaplama()

# Profil calistir
pr = cProfile.Profile()
pr.enable()
ana()
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
ps.print_stats(10)
print(s.getvalue())
