# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.8. Modüller, Paketler ve Import Sistemi
# Kitap  : Kod 1.221 (Import Biçimleri) · Kod 1.222 (Modüller, Paketler ve Import Sistemi) · Kod 1.223 (Yerleşik (Standart) Kütüphane Modülleri) · Kod 1.224 (Sys — Python yorumlayıcı bilgisi) · Kod 1.225 (Math — matematiksel fonksiyonlar) · Kod 1.226 (__name__ == '__main__' deseni) · Kod 1.227 (Paket Yapısı) · Kod 1.228 (Importlib: Dinamik Import) · Kod 1.229 (Importlib: Dinamik Import)
# Dosya : bolum01/01_05_08_moduller-paketler-ve-import-sistemi.py
# ==========================================================================
import sys
import os
import importlib
import math

# ─── Import Biçimleri ─────────────────────────────────────────────────────────
import math                          # Tam modülü içe aktar
from math import pi, e, sqrt        # Belirli isimleri içe aktar
from math import factorial as fakt  # Takma adla
import os.path as osp               # Alt modül takma adı
# from math import *   ← KÖTÜ UYGULAMA: ad alanını kirletir

print(f"math.pi  = {math.pi:.6f}")
print(f"pi       = {pi:.6f}")
print(f"fakt(10) = {fakt(10)}")

# ─── sys.path: Python modül arama yolu ────────────────────────────────────────
print("\n─── Python Modül Arama Yolları (sys.path) ──────────────────")
for i, yol in enumerate(sys.path[:5]):  # ilk 5'i göster
    print(f"  [{i}] {yol}")

# ─── Yerleşik (Standart) Kütüphane Modülleri ─────────────────────────────────
print("\n─── Standart Kütüphane Örnekleri ──────────────────────────")

# os — işletim sistemi arayüzü
print(f"os.getcwd()     : {os.getcwd()}")
print(f"os.cpu_count()  : {os.cpu_count()}")
print(f"os.path.join()  : {os.path.join('/ev', 'kullanici', 'proje')}")

# sys — Python yorumlayıcı bilgisi
print(f"sys.version     : {sys.version.split()[0]}")
print(f"sys.platform    : {sys.platform}")
print(f"sys.maxsize     : {sys.maxsize:,}")

# math — matematiksel fonksiyonlar
print(f"\nmath.sqrt(2)    : {math.sqrt(2):.10f}")
print(f"math.log(math.e): {math.log(math.e):.10f}")
print(f"math.floor(-2.7): {math.floor(-2.7)}")
print(f"math.ceil(-2.7) : {math.ceil(-2.7)}")
print(f"math.comb(10,3) : {math.comb(10,3)}")  # C(10,3) = 120

# ─── __name__ == '__main__' deseni ───────────────────────────────────────────
# Bu blok yalnızca dosya doğrudan çalıştırıldığında çalışır
# import edildiğinde çalışmaz — önemli bir Python deseni!
print("\n─── __name__ Deseni ────────────────────────────────────────")
print(f"Bu dosyadaki __name__ = '{__name__}'")
# if __name__ == '__main__':
#     # Ana program kodu burada
#     main()

# ─── Paket Yapısı ─────────────────────────────────────────────────────────────
# Örnek proje yapısı:
# veri_madenciligi/
# ├── __init__.py      ← paketi tanımlar
# ├── on_isleme.py
# ├── modeller/
# │   ├── __init__.py
# │   ├── siniflandirma.py
# │   └── kumeleme.py
# └── utils/
#     ├── __init__.py
#     └── gorsel.py

# ─── importlib: Dinamik Import ───────────────────────────────────────────────
modul_adi = 'math'
modul = importlib.import_module(modul_adi)
print(f"\nDinamik import: {modul_adi}.sin(π/2) = {modul.sin(modul.pi/2):.4f}")
