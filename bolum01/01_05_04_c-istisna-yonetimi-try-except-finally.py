# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.4. Kontrol Yapıları › C. İstisna Yönetimi: try/except/finally
# Kitap  : Kod 1.171 (İstisna Yönetimi: try/except/finally) · Kod 1.172 (İstisna Yönetimi: try/except/finally) · Kod 1.173 (B. for Döngüsü: İterasyon Protokolü) · Kod 1.174 (Enumerate: indeks ve değer birlikte) · Kod 1.175 (Zip: birden fazla koleksiyonu eşle) · Kod 1.176 (Break ve continue) · Kod 1.177 (İstisna Yönetimi: try/except/finally) · Kod 1.178 (While Döngüsü) · Kod 1.179 (İstisna Yönetimi: try/except/finally) · Kod 1.180 (İstisna Yönetimi: try/except/finally) · Kod 1.181 (İstisna Yönetimi: try/except/finally) · Kod 1.182 (İstisna Yönetimi: try/except/finally) · Kod 1.183 (İstisna Yönetimi: try/except/finally) · Kod 1.184 (İstisna Yönetimi: try/except/finally)
# Dosya : bolum01/01_05_04_c-istisna-yonetimi-try-except-finally.py
# ==========================================================================
# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
import math

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# ─── A. if / elif / else ───────────────────────────────────────────────────────
def bmi_siniflandir(kilo_kg, boy_m):
    """
    BMI = Ağırlık(kg) / Boy²(m²)  →  formül (1.6)
    Dünya Sağlık Örgütü sınıflandırması
    """
    bmi = kilo_kg / boy_m ** 2

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
    if bmi < 18.5:
        sinif = "Zayıf"
    elif 18.5 <= bmi < 25:
        sinif = "Normal"
    elif 25 <= bmi < 30:
        sinif = "Fazla Kilolu"
    elif 30 <= bmi < 35:
        sinif = "Obez (Sınıf I)"
    elif 35 <= bmi < 40:
        sinif = "Obez (Sınıf II)"
    else:
        sinif = "Morbid Obez (Sınıf III)"

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
    return bmi, sinif

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# Üçlü operatör (ternary): değer_true if koşul else değer_false
def mutlak_deger(x):
    return x if x >= 0 else -x

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
print("─── BMI Sınıflandırma ─────────────────────────────────────")
for kilo, boy in [(50,1.70),(70,1.70),(90,1.70),(110,1.70),(130,1.70)]:
    bmi, sinif = bmi_siniflandir(kilo, boy)
    print(f"  {kilo}kg/{boy}m  →  BMI = {bmi:.1f}  ({sinif})")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# ─── B. for Döngüsü: İterasyon Protokolü ─────────────────────────────────────
# McKinney (2022): "for döngüleri bir koleksiyon veya yineleyici üzerinde iterasyon içindir"
sayilar = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# range() — bellek verimli sayı dizisi
# range(baslangic, bitis, adim) → [baslangic, bitis) yarı açık aralık
print("\n─── for Döngüsü Desenleri ─────────────────────────────────")
toplam = sum(range(1, 101))  # Gauss formülü: n(n+1)/2 = 5050
gauss  = 100 * 101 // 2
print(f"  Σ(1..100) = {toplam} == {gauss} (Gauss): {toplam == gauss}")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# enumerate: indeks ve değer birlikte
print("\n  enumerate örneği:")
for i, deger in enumerate(sayilar[:5], start=1):
    print(f"    [{i}] = {deger}")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# zip: birden fazla koleksiyonu eşle
isimler = ['Ali', 'Veli', 'Ayşe']
notlar  = [85, 72, 93]
print("\n  zip ile paralel iterasyon:")
for isim, not_ in zip(isimler, notlar):
    print(f"    {isim}: {not_}")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# break ve continue
print("\n  break/continue — 3'e bölünebilen ilk asal:")
def asal_mi(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
for n in range(100, 200):
    if n % 3 != 0:
        continue      # 3'e bölünemiyorsa atla
    if asal_mi(n):
        print(f"    {n} (3'e bölünebilen asal bulunamadı)")
        break         # Bulunca dur
else:
    print("    Döngü tamamlandı (break olmadı)")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# ─── while Döngüsü ────────────────────────────────────────────────────────────
print("\n─── Newton-Raphson Karekök (while döngüsü) ────────────────")
def karekök_nr(S, hassasiyet=1e-10):
    """
    Newton-Raphson: x_{n+1} = (x_n + S/x_n) / 2
    f(x) = x² - S = 0  →  formül (1.7)
    """
    x = S / 2   # başlangıç tahmini
    iterasyon = 0
    while abs(x * x - S) > hassasiyet:
        x = (x + S / x) / 2
        iterasyon += 1
    return x, iterasyon

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
for S in [2, 9, 144, 10000]:
    kök, it = karekök_nr(S)
    print(f"  √{S:<6} = {kök:.10f}  (math.sqrt={math.sqrt(S):.10f}, {it} iterasyon)")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# ─── C. İstisna Yönetimi: try/except/else/finally ───────────────────────────
# McKinney (2022): "Hataları veya istisnaları zarif biçimde işlemek güçlü\n# programlar oluşturmanın önemli bir parçasıdır"
print("\n─── İstisna Yönetimi ───────────────────────────────────────")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
def guvenli_bolme(a, b):
    """Çok kademeli istisna yönetimi."""
    try:
        sonuc = a / b
    except ZeroDivisionError:
        print(f"  Hata: {a}/{b} — sıfıra bölme!")
        return None
    except TypeError as e:
        print(f"  Hata: Uyumsuz tip — {e}")
        return None
    else:
        print(f"  {a}/{b} = {sonuc:.4f}")  # yalnızca başarı durumunda
        return sonuc
    finally:
        print(f"  (her durumda çalışır)")  # her zaman

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
guvenli_bolme(10, 3)
guvenli_bolme(5, 0)
guvenli_bolme("a", 2)

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
# Özel istisna sınıfı tanımlama
class VeriDogrulamaHatasi(ValueError):
    """Özel hata sınıfı — OOP ile bağlantı"""
    def __init__(self, alan, deger, aciklama):
        self.alan = alan
        self.deger = deger
        super().__init__(f"{alan}={deger!r}: {aciklama}")

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
def yas_dogrula(yas):
    if not isinstance(yas, int):
        raise VeriDogrulamaHatasi('yas', yas, 'int olmalı')
    if not 0 <= yas <= 150:
        raise VeriDogrulamaHatasi('yas', yas, '[0, 150] aralığında olmalı')
    return True

# --- ▌ Kod Örneği 1.5.4 — Kontrol Yapıları: Kapsamlı Örnekler ---
for test_yas in [25, -5, 200, 3.5]:
    try:
        yas_dogrula(test_yas)
        print(f"  Yaş {test_yas}: Geçerli ✓")
    except VeriDogrulamaHatasi as e:
        print(f"  Yaş {test_yas}: {e}")
