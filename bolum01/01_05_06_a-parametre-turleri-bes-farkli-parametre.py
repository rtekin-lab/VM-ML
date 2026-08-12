# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.6. Fonksiyonlar ve Fonksiyonel Programlama › A. Parametre Türleri: Beş Farklı Parametre
# Kitap  : Kod 1.202 (Parametre Türleri: Beş Farklı Parametre) · Kod 1.203 (Sorted ile lambda) · Kod 1.204 (Map, filter, reduce ile lambda) · Kod 1.205 (C. Closure (Kapama)) · Kod 1.206 (Parametre Türleri: Beş Farklı Parametre) · Kod 1.207 (Parametre Türleri: Beş Farklı Parametre) · Kod 1.208 (Parametre Türleri: Beş Farklı Parametre) · Kod 1.209 (Parametre Türleri: Beş Farklı Parametre) · Kod 1.210 (E. Generator Fonksiyonları) · Kod 1.211 (Generator yalnızca talep üzerine değer üreti) · Kod 1.212 (Generator expression — liste comprehension'ı) · Kod 1.213 (Generator expression — liste comprehension'ı)
# Dosya : bolum01/01_05_06_a-parametre-turleri-bes-farkli-parametre.py
# ==========================================================================
import functools
import time
from typing import Callable, TypeVar, Any

# ─── A. Parametre Türleri ─────────────────────────────────────────────────────
def kapsamli_fonk(
    zorunlu,                   # Konumsal zorunlu
    varsayimli=10,             # Varsayılan değerli
    *args,                     # Değişken sayıda konumsal
    anahtar_kelime,            # Yalnızca keyword
    **kwargs                   # Değişken sayıda keyword
):
    """
    Tüm parametre türlerini sergileyen örnek fonksiyon.
    Docstring (PEP 257): fonksiyonu belgelemek için kullanılır.
    """
    print(f"zorunlu     : {zorunlu}")
    print(f"varsayimli  : {varsayimli}")
    print(f"args        : {args}")
    print(f"anahtar_kelime: {anahtar_kelime}")
    print(f"kwargs      : {kwargs}")

kapsamli_fonk("veri", 20, 1, 2, 3, anahtar_kelime="bilim", renk="mavi")

# ─── B. Lambda Fonksiyonları ──────────────────────────────────────────────────
# Anonim, tek ifadeli fonksiyonlar
kare = lambda x: x ** 2
topla = lambda x, y: x + y
print(f"\nLambda kare(5) = {kare(5)}")

# sorted ile lambda
ogrenciler = [('Ali', 85), ('Veli', 72), ('Ayşe', 93), ('Fatma', 88)]
sirali = sorted(ogrenciler, key=lambda x: x[1], reverse=True)
print(f"Not sırası: {sirali}")

# map, filter, reduce ile lambda
sayilar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
kareler  = list(map(lambda x: x**2, sayilar))
ciftler  = list(filter(lambda x: x % 2 == 0, sayilar))
toplam   = functools.reduce(lambda a, b: a + b, sayilar)
print(f"\nmap(kare)   : {kareler}")
print(f"filter(çift): {ciftler}")
print(f"reduce(+)   : {toplam}")

# ─── C. Closure (Kapama) ─────────────────────────────────────────────────────
# Closure: iç fonksiyonun dış fonksiyonun değişkenlerini "yakalaması"
def katsayi_ureten(katsayi):
    def carpmak(x):
        return x * katsayi  # 'katsayi' dış kapsamdan yakalanır
    return carpmak

iki_kati  = katsayi_ureten(2)
uc_kati   = katsayi_ureten(3)
bes_kati  = katsayi_ureten(5)

print(f"\nClosure: iki_kati(7) = {iki_kati(7)}")
print(f"Closure: uc_kati(7)  = {uc_kati(7)}")

# ─── D. Dekoratörler (Decorators) ────────────────────────────────────────────
# Dekoratör: başka bir fonksiyonu saran (wrap eden) fonksiyon
def zamanlayici(fonk):
    """Fonksiyon yürütme süresini ölçer."""
    @functools.wraps(fonk)  # orijinal fonksiyon meta verisini korur
    def sarici(*args, **kwargs):
        baslangic = time.perf_counter()
        sonuc = fonk(*args, **kwargs)
        sure = time.perf_counter() - baslangic
        print(f"  ⏱ {fonk.__name__}(): {sure*1000:.3f} ms")
        return sonuc
    return sarici

def onbellek(fonk):
    """Memoization — önceki sonuçları önbelleğe alır."""
    bellek = {}
    @functools.wraps(fonk)
    def sarici(*args):
        if args not in bellek:
            bellek[args] = fonk(*args)
        return bellek[args]
    return sarici

@zamanlayici
@onbellek
def fibonacci(n):
    """Fibonacci dizisi — özyinelemeli (recursive)."""
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

print("\n─── Dekoratör Zinciri ──────────────────────────────────────")
sonuc = fibonacci(35)
print(f"fibonacci(35) = {sonuc}")

# functools.lru_cache — yerleşik memoization dekoratörü
@functools.lru_cache(maxsize=128)
def hiz_katsayisi(n):
    if n == 0: return 1
    return n * hiz_katsayisi(n-1)

# ─── E. Generator Fonksiyonları ───────────────────────────────────────────────
# McKinney (2022): "Bir üreteç (generator) ... yield anahtar kelimesini kullanır"
def sonsuz_fibonacci():
    """Sonsuz Fibonacci üreteci — bellek verimli."""
    a, b = 0, 1
    while True:
        yield a          # değeri üretir, ama fonksiyon askıya alınır
        a, b = b, a + b

# Generator yalnızca talep üzerine değer üretir (lazy evaluation)
gen = sonsuz_fibonacci()
fib_100 = [next(gen) for _ in range(10)]
print(f"\nFibonacci (ilk 10): {fib_100}")

# Generator expression — liste comprehension'ın bellek verimli hali
n = 10_000_000
# Liste: tüm değerleri belleğe alır
# list_sum  = sum([x**2 for x in range(n)])  # ~80MB bellek!
# Generator: birer birer üretir
gen_sum   = sum(x**2 for x in range(n))    # ~200 byte bellek!
print(f"Σ(x²) [0,{n}): {gen_sum}")
