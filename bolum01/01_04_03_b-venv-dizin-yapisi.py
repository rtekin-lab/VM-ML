# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.3. venv — Python'ın Yerleşik Sanal Ortam Modülü › B. venv Dizin Yapısı
# Kitap  : Kod 1.86 (Site-packages dizinini bul) · Kod 1.87 (Pyvenv.cfg içeriğini oku) · Kod 1.88 (Kurulu paketlerin listesi) · Kod 1.89 (Kurulu paketlerin listesi)
# Dosya : bolum01/01_04_03_b-venv-dizin-yapisi.py
# ==========================================================================
# --- ▌ Kod Örneği 1.4.2 — venv Dizin Yapısı Analizi ---
import os
import sys

# --- ▌ Kod Örneği 1.4.2 — venv Dizin Yapısı Analizi ---
# Mevcut ortam dizin yapısını incele
if hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix:
    print(f"Ortam kökü    : {sys.prefix}")
    print(f"Sistem Python : {sys.base_prefix}")
    print(f"Python yolu   : {sys.executable}")
    print(f"İzole ortam   : {'EVET' if sys.prefix != sys.base_prefix else 'HAYIR'}")

# --- ▌ Kod Örneği 1.4.2 — venv Dizin Yapısı Analizi ---
    # site-packages dizinini bul
    import site
    sp = site.getsitepackages()
    print(f"site-packages : {sp[0]}")

# --- ▌ Kod Örneği 1.4.2 — venv Dizin Yapısı Analizi ---
    # pyvenv.cfg içeriğini oku
    cfg_yolu = os.path.join(sys.prefix, 'pyvenv.cfg')
    if os.path.exists(cfg_yolu):
        print("\n─── pyvenv.cfg İçeriği ───")
        with open(cfg_yolu) as f:
            print(f.read())
else:
    print("Aktif sanal ortam bulunamadı.")
    print(f"Sistem Python: {sys.executable}")

# --- ▌ Kod Örneği 1.4.2 — venv Dizin Yapısı Analizi ---
# Kurulu paketlerin listesi
# pkg_resources Python 3.12+ ile gelmiyor; standart kutuphanedeki
# importlib.metadata ayni bilgiyi verir ve onerilen yoldur.
from importlib.metadata import distributions
paketler = sorted(distributions(), key=lambda dd: dd.metadata["Name"].lower())
print(f"\n─── Kurulu Paketler ({len(paketler)} adet) ───")
for pkg in paketler[:10]:
    print(f"  {pkg.metadata['Name']:<25} {pkg.version}")
