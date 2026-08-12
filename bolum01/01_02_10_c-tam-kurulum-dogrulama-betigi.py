# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.10. requirements.txt ve environment.yml ile Bağımlılık Yönetimi › C. Tam Kurulum Doğrulama Betiği
# Kitap  : Kod 1.62 (Tam kurulum doğrulama betiği) · Kod 1.63 (Tam kurulum doğrulama betiği) · Kod 1.64 (Tam kurulum doğrulama betiği) · Kod 1.65 (Tam kurulum doğrulama betiği) · Kod 1.66 (Tam kurulum doğrulama betiği) · Kod 1.67 (Tam kurulum doğrulama betiği)
# Dosya : bolum01/01_02_10_c-tam-kurulum-dogrulama-betigi.py
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
from scipy import stats
"""
veri_bilimi_kurulum_dogrulama.py
Tüm temel kütüphanelerin kurulumunu ve temel işlevselliğini doğrular.
"""
import sys

def renk(metin, kod):
    return f"\033[{kod}m{metin}\033[0m"

def basarili(msg): print(renk(f"  ✓ {msg}", '32'))
def hatali(msg):   print(renk(f"  ✗ {msg}", '31'))
def uyari(msg):    print(renk(f"  ⚠ {msg}", '33'))

print("=" * 55)
print("  PYTHON VERİ BİLİMİ ORTAMI DOĞRULAMA RAPORU")
print("=" * 55)
print(f"Python sürümü: {sys.version.split()[0]}")

gerekli = {
    'numpy'       : ('1.24', lambda: __import__('numpy').array([1,2,3]).mean()),
    'pandas'      : ('2.0',  lambda: __import__('pandas').DataFrame({'a':[1,2]})['a'].mean()),
    'matplotlib'  : ('3.7',  lambda: __import__('matplotlib').__version__),
    'scipy'       : ('1.11', lambda: __import__('scipy').stats.norm.pdf(0)),
    'sklearn'     : ('1.3',  lambda: __import__('sklearn').__version__),
    'statsmodels' : ('0.14', lambda: __import__('statsmodels').__version__),
    'seaborn'     : ('0.12', lambda: __import__('seaborn').__version__),
    'IPython'     : ('8.0',  lambda: __import__('IPython').__version__),
    'jupyterlab'  : ('4.0',  lambda: __import__('jupyterlab').__version__),
}

isteğe_bağlı = ['plotly', 'missingno', 'yfinance', 'requests',
                 'beautifulsoup4', 'sqlalchemy']

hatali_sayisi = 0
print("\n─── ZORUNLU KÜTÜPHANEler ───────────────────────────────")
for paket, (min_ver, test_fn) in gerekli.items():
    try:
        mod = __import__(paket.replace('-', '_'))
        ver = getattr(mod, '__version__', '?')
        test_fn()
        basarili(f"{paket:<15} v{ver}")
    except ImportError:
        hatali(f"{paket:<15} BULUNAMADI → pip install {paket}")
        hatali_sayisi += 1
    except Exception as e:
        uyari(f"{paket:<15} İşlevsellik hatası: {e}")

print("\n─── İSTEĞE BAĞLI KÜTÜPHANEler ─────────────────────────")
for paket in isteğe_bağlı:
    try:
        mod = __import__(paket.replace('-', '_'))
        ver = getattr(mod, '__version__', '?')
        basarili(f"{paket:<20} v{ver}")
    except ImportError:
        uyari(f"{paket:<20} kurulu değil → pip install {paket}")

print("\n─── ÖZET ─────────────────────────────────────────────")
if hatali_sayisi == 0:
    print(renk("  ✓ Tüm zorunlu kütüphaneler kurulu ve çalışıyor!", '32'))
else:
    print(renk(f"  ✗ {hatali_sayisi} zorunlu kütüphane eksik — yukarıdaki komutlarla kurun.", '31'))
print("=" * 55)
