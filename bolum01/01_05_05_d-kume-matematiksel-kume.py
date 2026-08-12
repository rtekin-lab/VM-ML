# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.5. Yerleşik Veri Yapıları › D. Küme (set): Matematiksel Küme
# Kitap  : Kod 1.185 (Dilimleme (slicing): liste[başlangıç:bitiş:A) · Kod 1.186 (Temel liste metodları) · Kod 1.187 (Sort vs sorted: yerinde vs yeni liste) · Kod 1.188 (Küme (set): Matematiksel Küme) · Kod 1.189 (Zaman karmaşıklığı karşılaştırması) · Kod 1.190 (Küme (set): Matematiksel Küme) · Kod 1.191 (Çoklu atama (tuple unpacking)) · Kod 1.192 (Yıldızlı unpacking (Python 3+)) · Kod 1.193 (Tuple boyutu list'ten küçük) · Kod 1.194 (C. DICT — Hash Tablosu) · Kod 1.195 (Erişim) · Kod 1.196 (Defaultdict — var olmayan anahtar için varsa) · Kod 1.197 (Counter — en yaygın n eleman) · Kod 1.198 (Dict Comprehension) · Kod 1.199 (Küme (set): Matematiksel Küme) · Kod 1.200 (Frozenset — değişmez küme (sözlük anahtarı o) · Kod 1.201 (Frozenset — değişmez küme (sözlük anahtarı o)
# Dosya : bolum01/01_05_05_d-kume-matematiksel-kume.py
# ==========================================================================
import sys
import time
from collections import defaultdict, Counter, OrderedDict, deque

# ══════════════════════════════════════════════════════════════════════════════
# A. LIST — Dinamik Dizi
# ══════════════════════════════════════════════════════════════════════════════
print("─── A. Liste ───────────────────────────────────────────────")
# Oluşturma
liste = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# Dilimleme (slicing): liste[baslangic:bitis:adim]
print(f"Orijinal    : {liste}")
print(f"[2:7]       : {liste[2:7]}")         # 3.den 7.ye (hariç)
print(f"[::-1]      : {liste[::-1]}")         # ters çevir
print(f"[::2]       : {liste[::2]}")          # çift indeksler
print(f"[-3:]       : {liste[-3:]}")          # son 3 eleman

# Temel liste metodları
liste.append(7)          # sona ekle          O(1)
liste.insert(0, 0)       # başa ekle          O(n)
cikti = liste.pop()      # sondan çıkar       O(1)
liste.remove(1)          # ilk 1'i sil        O(n)
liste.sort()             # yerinde sırala     O(n log n) — Timsort
print(f"Sıralı      : {liste}")
liste.sort(reverse=True) # azalan sırala

# sort vs sorted: yerinde vs yeni liste
orijinal = [3,1,4,1,5]
sirali_kopya = sorted(orijinal, key=lambda x: -x)
print(f"Orijinal (değişmedi): {orijinal}")
print(f"sorted():  {sirali_kopya}")

# List Comprehension — McKinney (2022) "Python'ın en sevilen özelliklerinden biri"
kareler = [x**2 for x in range(10)]
ciftler = [x for x in range(20) if x % 2 == 0]
matris  = [[i*j for j in range(1,5)] for i in range(1,5)]
print(f"Kareler : {kareler}")
print(f"Çiftler : {ciftler}")
print(f"Matris  :")
for satir in matris:
    print(f"  {satir}")

# Zaman karmaşıklığı karşılaştırması
n = 100_000
lst = list(range(n))
s_lst = set(lst)

t0 = time.perf_counter()
_ = (n-1) in lst    # O(n) — tüm listeyi tarar
t_liste = time.perf_counter() - t0

t0 = time.perf_counter()
_ = (n-1) in s_lst  # O(1) — hash tablosu
t_kume  = time.perf_counter() - t0

print(f"\nArama ({n} elem): Liste={t_liste*1e6:.1f}µs, Küme={t_kume*1e6:.1f}µs")

# ══════════════════════════════════════════════════════════════════════════════
# B. TUPLE — Değişmez Dizi
# ══════════════════════════════════════════════════════════════════════════════
print("\n─── B. Demet (Tuple) ────────────────────────────────────────")
# McKinney (2022): "sabit uzunluklu, değişmez Python nesneleri dizisi"
koordinat = (41.0082, 28.9784)   # İstanbul koordinatı
x, y = koordinat                 # unpacking (açma)
print(f"Koordinat: lat={x}, lon={y}")

# Çoklu atama (tuple unpacking)
a, b = 10, 20
a, b = b, a   # yer değiştirme — swap
print(f"Swap sonrası: a={a}, b={b}")

# Yıldızlı unpacking (Python 3+)
ilk, *orta, son = [1, 2, 3, 4, 5, 6]
print(f"ilk={ilk}, orta={orta}, son={son}")

# Named tuple — daha okunabilir
from collections import namedtuple
Nokta = namedtuple('Nokta', ['x', 'y', 'z'])
p = Nokta(1.5, 2.3, 0.8)
print(f"Nokta: x={p.x}, y={p.y}, z={p.z}")

# Tuple boyutu list'ten küçük
lst_mem = sys.getsizeof([1,2,3,4,5])
tup_mem = sys.getsizeof((1,2,3,4,5))
print(f"[1..5] boyut: {lst_mem} byte, (1..5) boyut: {tup_mem} byte")

# ══════════════════════════════════════════════════════════════════════════════
# C. DICT — Hash Tablosu
# ══════════════════════════════════════════════════════════════════════════════
print("\n─── C. Sözlük (Dict) ────────────────────────────────────────")
# Python 3.7+: ekleme sırası korunur
ogrenci = {
    'ad': 'Ahmet', 'soyad': 'Yılmaz',
    'notlar': [85, 92, 78, 95], 'aktif': True
}

# Erişim
print(f"Ad: {ogrenci['ad']}")
print(f"Ortalama: {sum(ogrenci['notlar'])/len(ogrenci['notlar']):.2f}")

# .get() — KeyError yerine varsayılan
print(f"Şehir: {ogrenci.get('şehir', 'Belirtilmemiş')}")

# Güncelleme
ogrenci.update({'sehir': 'İstanbul', 'gpa': 3.7})

# Döngü yöntemleri
print("\nAnahtarlar:", list(ogrenci.keys()))
print("Çiftler:")
for anahtar, deger in ogrenci.items():
    print(f"  {anahtar}: {deger}")

# defaultdict — var olmayan anahtar için varsayılan değer
kelime_freq = defaultdict(int)
metin = "python veri bilimi python veri python"
for kelime in metin.split():
    kelime_freq[kelime] += 1
print(f"\nKelime Frekansı: {dict(kelime_freq)}")

# Counter — en yaygın n eleman
sayac = Counter("abcabcaaabbb")
print(f"Counter: {sayac}")
print(f"En yaygın 3: {sayac.most_common(3)}")

# Dict Comprehension
kare_sozluk = {x: x**2 for x in range(1, 8)}
print(f"\nKare sözlüğü: {kare_sozluk}")

# ══════════════════════════════════════════════════════════════════════════════
# D. SET — Matematiksel Küme
# ══════════════════════════════════════════════════════════════════════════════
print("\n─── D. Küme (Set) ────────────────────────────────────────────")
A = {1, 2, 3, 4, 5, 6}
B = {4, 5, 6, 7, 8, 9}

print(f"A = {A}")
print(f"B = {B}")
print(f"A ∪ B (birleşim)   : {A | B}")        # union
print(f"A ∩ B (kesişim)    : {A & B}")        # intersection
print(f"A \\ B (fark)        : {A - B}")       # difference
print(f"A △ B (simetrik)   : {A ^ B}")        # symmetric difference
print(f"A ⊆ B (alt küme mi): {A <= B}")       # subset
print(f"A ⊃ B (üst küme mi): {A > B}")        # proper superset

# frozenset — değişmez küme (sözlük anahtarı olabilir)
fs = frozenset([1, 2, 3])
sozluk = {fs: "değişmez küme anahtarı"}
print(f"frozenset anahtar: {sozluk}")
