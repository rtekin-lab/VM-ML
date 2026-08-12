# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.1. Python'a Giriş: Dil Tasarım Felsefesi › B. Bellek Modeli: Her Şey Bir Nesnedir
# Kitap  : Kod 1.141 (Id(): Nesnenin bellek adresini döndürür) · Kod 1.142 (Gerçek kopya için: copy veya dilimleme) · Kod 1.143 (Tıp Sistemi: Her Şey Bir Nesnedir) · Kod 1.144 (Küçük Tamsayı Önbelleği (-5 ila 256)) · Kod 1.145 (Bellek Modeli: Her Şey Bir Nesnedir) · Kod 1.146 (Bellek Modeli: Her Şey Bir Nesnedir) · Kod 1.147 (Bellek Modeli: Her Şey Bir Nesnedir)
# Dosya : bolum01/01_05_01_b-bellek-modeli-her-sey-bir-nesnedir.py
# ==========================================================================
# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
import sys

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# ─── Python Bellek Modeli: Referans Semantiği ─────────────────────────────────
a = [1, 2, 3]
b = a              # b, a ile AYNI nesneyi işaret eder (kopya değil!)
b.append(4)
print(f"a = {a}")  # [1, 2, 3, 4]  — a da değişti!
print(f"b = {b}")  # [1, 2, 3, 4]

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# id(): Nesnenin bellek adresini döndürür
print(f"id(a) = {id(a)}")
print(f"id(b) = {id(b)}")
print(f"a is b: {a is b}")  # True — aynı nesne!

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# Gerçek kopya için: copy veya dilimleme
c = a.copy()
c.append(5)
print(f"a sonra = {a}")  # [1, 2, 3, 4] — değişmedi
print(f"c = {c}")        # [1, 2, 3, 4, 5]

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# ─── Tip Sistemi: Her Şey Bir Nesnedir ───────────────────────────────────────
ornek_degerler = [42, 3.14, "merhaba", True, None, [1,2], (1,2), {1,2}, {'a':1}]

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
print(f"{'Değer':<15} {'Tip':<20} {'Boyut (byte)':<15} {'id'}")
print("-" * 70)
for v in ornek_degerler:
    print(f"{str(v):<15} {type(v).__name__:<20} {sys.getsizeof(v):<15} {id(v)}")

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# ─── Küçük Tamsayı Önbelleği (-5 ila 256) ────────────────────────────────────
# CPython optimizasyonu: sık kullanılan küçük sayıları önbelleğe alır
x = 256; y = 256
print(f"\nx is y (256): {x is y}")  # True — önbellekten aynı nesne

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
x = 257; y = 257
print(f"x is y (257): {x is y}")    # False — önbellekte yok, farklı nesneler

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
# ─── Tür Doğrulama ───────────────────────────────────────────────────────────
def tip_goster(deger):
    print(f"Değer: {deger!r:<20} Tip: {type(deger).__name__:<12} "
          f"isinstance(int): {isinstance(deger, (int, float))}")

# --- ▌ Kod Örneği 1.5.1 — Python Bellek Modeli ve Nesne Kimliği ---
tip_goster(42)
tip_goster(3.14)
tip_goster("Python")
tip_goster(True)    # bool, int'in alt sınıfıdır!
print(f"\nisinstance(True, int): {isinstance(True, int)}")  # True
