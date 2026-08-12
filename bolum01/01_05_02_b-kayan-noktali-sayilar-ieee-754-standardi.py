# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.2. Değişkenler, Veri Tipleri ve Tür Sistemi › B. Kayan Noktalı Sayılar (float): IEEE 754 Standardı
# Kitap  : Kod 1.148 (Tam Sayılar: Keyfi Kesinlik) · Kod 1.149 (Faktöriyel hesaplama (taşma yok!)) · Kod 1.150 (Kayan Nokta: IEEE 754 Temsil Sorunu) · Kod 1.151 (Doğru karşılaştırma: math.isclose veya round) · Kod 1.152 (Float'ın ikili temsili) · Kod 1.153 (IEEE 754 sınırları) · Kod 1.154 (Yüksek kesinlik: Decimal modülü) · Kod 1.155 (String: Değişmez Karakter Dizisi) · Kod 1.156 (Kayan Noktalı Sayılar (float): IEEE 754 Stan) · Kod 1.157 (String formatlama yöntemleri) · Kod 1.158 (Boolean ve None) · Kod 1.159 (Falsy değerler: False, 0, 0.0, '', [], {}, () · Kod 1.160 (Tür Dönüşümleri (Type Casting)) · Kod 1.161 (Tür Dönüşümleri (Type Casting))
# Dosya : bolum01/01_05_02_b-kayan-noktali-sayilar-ieee-754-standardi.py
# ==========================================================================
import sys
import struct
from decimal import Decimal
from fractions import Fraction

# ─── Tam Sayılar: Keyfi Kesinlik ──────────────────────────────────────────────
buyuk_sayi = 2 ** 100
print(f"2^100 = {buyuk_sayi}")
print(f"Rakam sayısı: {len(str(buyuk_sayi))}")

# Faktöriyel hesaplama (taşma yok!)
def faktoriyel(n):
    sonuc = 1
    for i in range(2, n + 1):
        sonuc *= i
    return sonuc
print(f"100! = {faktoriyel(100)}")  # 158 basamaklı sayı

# ─── Kayan Nokta: IEEE 754 Temsil Sorunu ─────────────────────────────────────
# Neden 0.1 + 0.2 ≠ 0.3?
print(f"\n0.1 + 0.2 = {0.1 + 0.2}")          # 0.30000000000000004
print(f"0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")  # False!

# Doğru karşılaştırma: math.isclose veya round
import math
print(f"isclose: {math.isclose(0.1 + 0.2, 0.3)}")   # True
print(f"round:   {round(0.1 + 0.2, 10) == round(0.3, 10)}")

# float'ın ikili temsili
x = 0.1
packed = struct.pack('d', x)
print(f"\n0.1'in ikili temsili (hex): {packed.hex()}")
print(f"Hassas değer: {x:.55f}")

# IEEE 754 sınırları
print(f"\nMaks float: {sys.float_info.max:.2e}")
print(f"Min float : {sys.float_info.min:.2e}")
print(f"Epsilon   : {sys.float_info.epsilon:.2e}")

# Yüksek kesinlik: Decimal modülü
d1 = Decimal('0.1')
d2 = Decimal('0.2')
d3 = Decimal('0.3')
print(f"\nDecimal: 0.1 + 0.2 = {d1 + d2}")
print(f"Decimal eşitlik: {d1 + d2 == d3}")  # True!

# ─── String: Değişmez Karakter Dizisi ────────────────────────────────────────
s1 = "Merhaba, Dünya!"
s2 = 'Python 3.11'
s3 = """Çok satırlı
string örneği"""
s4 = r"Ham string:\n(escape yok)"    # raw string
s5 = f"Pi ≈ {math.pi:.4f}"               # f-string (Python 3.6+)
s6 = b"Bayt dizisi"                        # bytes

print(f"\ns1.upper()    : {s1.upper()}")
print(f"s1.split(',') : {s1.split(',')}")
print(f"s1[0:7]       : {s1[0:7]}")       # dilimleme (slicing)
print(f"len(s1)       : {len(s1)}")
print(f"'ya' in s1    : {'ya' in s1}")

# String formatlama yöntemleri
pi = 3.14159265
print(f"%-format  : 'Pi = %.4f' % pi  → 'Pi = {pi:.4f}'")
print(f"str.format: 'Pi = {'{:.4f}'.format(pi)}'")
print(f"f-string  : f'Pi = {pi:.4f}'  → 'Pi = {pi:.4f}'")

# ─── Boolean ve None ──────────────────────────────────────────────────────────
print(f"\nbool alt sınıf mı? isinstance(True, int) = {isinstance(True, int)}")
print(f"True + 1 = {True + 1}")  # 2  (bool int'ten türer!)
print(f"True * 5 = {True * 5}")  # 5

# Falsy değerler: False, 0, 0.0, '', [], {}, (), set(), None
falsy = [False, 0, 0.0, '', [], {}, (), set(), None]
for v in falsy:
    print(f"  bool({str(v):<10}) = {bool(v)}")

# ─── Tür Dönüşümleri (Type Casting) ──────────────────────────────────────────
print("\n─── Tür Dönüşümleri ───────────────────────────────────────────────────")
donusumler = [
    ("'42' → int",   int('42')),
    ("'3.14' → float", float('3.14')),
    ("42 → str",     str(42)),
    ("42 → bool",    bool(42)),
    ("0 → bool",     bool(0)),
    ("[1,2] → tuple", tuple([1,2])),
    ("(1,2) → list",  list((1,2))),
    ("{1,2} → list",  list({1,2})),
]
for aciklama, sonuc in donusumler:
    print(f"  {aciklama:<20} → {sonuc!r}")
