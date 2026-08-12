# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.3. Operatörler ve İfadeler
# Kitap  : Kod 1.162 (// ve % ilişkisi: a = (a//b)*b + (a%b)) · Kod 1.163 (Divmod(): // ve % aynı anda) · Kod 1.164 (Mantıksal Operatörler: Kısa Devre Değerlendi) · Kod 1.165 (False or True → True değerlendirilir) · Kod 1.166 (Kimlik ve Üyelik Operatörleri) · Kod 1.167 (Operatörler ve İfadeler) · Kod 1.168 (Bit Düzeyinde Operatörler (Veri Biliminde Ma) · Kod 1.169 (Atama Operatörleri) · Kod 1.170 (Atama Operatörleri)
# Dosya : bolum01/01_05_03_operatorler-ve-ifadeler.py
# ==========================================================================
import operator

# ─── Aritmetik Operatörler ve Öncelik (PEMDAS) ───────────────────────────────
# Öncelik: ** > *, /, //, % > +, -
sonuc1 = 2 + 3 * 4 ** 2       # 2 + 3*16 = 50
sonuc2 = (2 + 3) * 4 ** 2     # 5*16 = 80
print(f"2 + 3 * 4**2     = {sonuc1}")
print(f"(2 + 3) * 4**2   = {sonuc2}")

# // ve % ilişkisi: a = (a//b)*b + (a%b)
a, b = 17, 5
print(f"\n{a} // {b} = {a//b}")
print(f"{a} %  {b} = {a%b}")
print(f"Doğrulama: {(a//b)*b + a%b} == {a}")  # 17 == 17

# divmod(): // ve % aynı anda
bolum, kalan = divmod(17, 5)
print(f"divmod(17,5) = ({bolum}, {kalan})")

# ─── Karşılaştırma Operatörleri ve Zincirleme ────────────────────────────────
x = 5
print(f"\n1 < x < 10       : {1 < x < 10}")     # True (Python'a özgü!)
print(f"1 < x and x < 10  : {1 < x and x < 10}") # eşdeğeri

# ─── Mantıksal Operatörler: Kısa Devre Değerlendirme ─────────────────────────
# McKinney (2022): "koşullar soldan sağa değerlendirilir ve kısa devre yapar"
def yan_etki(msg, sonuc):
    print(f"  '{msg}' değerlendirildi → {sonuc}")
    return sonuc

print("\nor kısa devre (False or True):")
# False or True → True değerlendirilir
sonuc = yan_etki("False", False) or yan_etki("True", True)

print("\nand kısa devre (False and True):")
# False and ... → True hiç değerlendirilmez!
sonuc = yan_etki("False", False) and yan_etki("True (DEĞERLENDİRİLMEDİ)", True)

# Kısa devre, güvenli erişim için kullanılır
liste = [1, 2, 3]
# Boş kontrolü: liste and liste[0]  (IndexError'dan kaçınır)
bos = []
deger = bos and bos[0]   # [] döner, IndexError yok
print(f"\nbos and bos[0] = {deger!r}")

# ─── Kimlik ve Üyelik Operatörleri ───────────────────────────────────────────
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"\na == b: {a == b}")  # True  — değer eşitliği
print(f"a is b: {a is b}")   # False — farklı nesneler
print(f"a is c: {a is c}")   # True  — aynı nesne

# in / not in: üyelik testi
koleksiyon = [1, 2, 3, 4, 5]
print(f"3 in koleksiyon     : {3 in koleksiyon}")
print(f"10 not in koleksiyon: {10 not in koleksiyon}")

# ─── Bit Düzeyinde Operatörler (Veri Biliminde Maske İşlemleri) ──────────────
# Pandas'ta filtreleme için kritik: & (and), | (or), ~ (not), ^ (xor)
a, b = 0b1010, 0b1100   # 10, 12
print(f"\n{a:04b} & {b:04b} = {a & b:04b} ({a & b})")   # AND
print(f"{a:04b} | {b:04b} = {a | b:04b} ({a | b})")   # OR
print(f"{a:04b} ^ {b:04b} = {a ^ b:04b} ({a ^ b})")   # XOR
print(f"~{a:04b}        = {~a} (tümleyen)")

# ─── Atama Operatörleri ───────────────────────────────────────────────────────
x = 10
x += 5;  print(f"\nx += 5  → x = {x}")  # 15
x -= 3;  print(f"x -= 3  → x = {x}")  # 12
x *= 2;  print(f"x *= 2  → x = {x}")  # 24
x //= 5; print(f"x //= 5 → x = {x}")  # 4
x **= 3; print(f"x **= 3 → x = {x}")  # 64
x %= 10; print(f"x %%= 10 → x = {x}")  # 4
