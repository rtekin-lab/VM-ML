# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.12. Veri Bilimi Perspektifinden Python: Bütünleşik Örnek
# Kitap  : Kod 1.262 (Merkezi Eğilim Ölçüleri) · Kod 1.263 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.264 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.265 (Yayılım Ölçüleri) · Kod 1.266 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.267 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.268 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.269 (Veri Sınıfı ile Özet Rapor) · Kod 1.270 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.271 (Veri Bilimi Perspektifinden Python: Bütünleş) · Kod 1.272 (İki değişken arası korelasyon)
# Dosya : bolum01/01_05_12_veri-bilimi-perspektifinden-python-butunlesik-or.py
# ==========================================================================
"""
Temel İstatistik Kütüphanesi — Sıfırdan Python
Grus (2015) "Data Science from Scratch" yaklaşımıyla
OOP, tip ipuçları, generator, lambda ve tüm temel konuları entegre eder.
"""
import math
import random
from typing import List, Tuple, Callable, Optional
from collections import Counter
from dataclasses import dataclass, field

# ─── Merkezi Eğilim Ölçüleri ─────────────────────────────────────────────────
def ortalama(veri: List[float]) -> float:
    """μ = (1/n) Σ xᵢ"""
    return sum(veri) / len(veri)

def medyan(veri: List[float]) -> float:
    """Sıralı verinin orta değeri."""
    n = len(veri)
    sirali = sorted(veri)
    orta = n // 2
    return sirali[orta] if n % 2 != 0 else (sirali[orta-1] + sirali[orta]) / 2

def mod(veri: List[float]) -> List[float]:
    """En sık görülen değer(ler)."""
    sayac = Counter(veri)
    maks_frek = max(sayac.values())
    return [k for k, v in sayac.items() if v == maks_frek]

# ─── Yayılım Ölçüleri ────────────────────────────────────────────────────────
def varyans(veri: List[float], populasyon: bool = False) -> float:
    """
    Örneklem: s² = Σ(xᵢ - x̄)² / (n-1)   [Bessel düzeltmesi]
    Popülasyon: σ² = Σ(xᵢ - μ)² / n
    """
    mu = ortalama(veri)
    n = len(veri)
    payda = n if populasyon else n - 1
    return sum((x - mu) ** 2 for x in veri) / payda

def standart_sapma(veri: List[float], populasyon: bool = False) -> float:
    return math.sqrt(varyans(veri, populasyon))

def yuzdelik(veri: List[float], p: float) -> float:
    """p. yüzdelik değer (0 ≤ p ≤ 100)."""
    assert 0 <= p <= 100
    sirali = sorted(veri)
    indeks = (p / 100) * (len(sirali) - 1)
    alt = int(indeks)
    kesir = indeks - alt
    if alt + 1 >= len(sirali):
        return sirali[alt]
    return sirali[alt] + kesir * (sirali[alt+1] - sirali[alt])

def ceyrekler_arasi_aralik(veri: List[float]) -> float:
    """IQR = Q3 - Q1"""
    return yuzdelik(veri, 75) - yuzdelik(veri, 25)

# ─── İlişki Ölçüleri ─────────────────────────────────────────────────────────
def kovaryans(x: List[float], y: List[float]) -> float:
    """Cov(X,Y) = Σ(xᵢ-x̄)(yᵢ-ȳ) / (n-1)"""
    assert len(x) == len(y), "Boyutlar eşit olmalı"
    mu_x, mu_y = ortalama(x), ortalama(y)
    n = len(x)
    return sum((xi-mu_x)*(yi-mu_y) for xi,yi in zip(x,y)) / (n-1)

def pearson_r(x: List[float], y: List[float]) -> float:
    """r = Cov(X,Y) / (σ_X × σ_Y)"""
    return kovaryans(x,y) / (standart_sapma(x) * standart_sapma(y))

# ─── Aykırı Değer Tespiti ─────────────────────────────────────────────────────
def iqr_aykiri_deger(veri: List[float],
                     katsayi: float = 1.5) -> Tuple[List[float], List[float]]:
    """
    Tukey (1977) kutu grafiği kuralı:
    [Q1 - k*IQR, Q3 + k*IQR] dışındaki değerler aykırı
    """
    q1 = yuzdelik(veri, 25)
    q3 = yuzdelik(veri, 75)
    iqr = q3 - q1
    alt_sinir = q1 - katsayi * iqr
    ust_sinir = q3 + katsayi * iqr
    normal   = [x for x in veri if alt_sinir <= x <= ust_sinir]
    aykiri   = [x for x in veri if x < alt_sinir or x > ust_sinir]
    return normal, aykiri

# ─── Veri Sınıfı ile Özet Rapor ─────────────────────────────────────────────
@dataclass
class IstatistikRaporu:
    veri_adi: str
    veri: List[float] = field(repr=False)

    @property
    def n(self) -> int: return len(self.veri)

    @property
    def mu(self) -> float: return ortalama(self.veri)

    @property
    def sigma(self) -> float: return standart_sapma(self.veri)

    @property
    def q1(self) -> float: return yuzdelik(self.veri, 25)

    @property
    def q3(self) -> float: return yuzdelik(self.veri, 75)

    def rapor_yazdir(self):
        _, aykiri = iqr_aykiri_deger(self.veri)
        print(f"\n{'='*55}")
        print(f"  {self.veri_adi} — İstatistik Raporu")
        print(f"{'='*55}")
        print(f"  n            = {self.n}")
        print(f"  Ortalama (μ) = {self.mu:.4f}")
        print(f"  Medyan       = {medyan(self.veri):.4f}")
        print(f"  Std Sapma (σ)= {self.sigma:.4f}")
        print(f"  Minimum      = {min(self.veri):.4f}")
        print(f"  Q1           = {self.q1:.4f}")
        print(f"  Q3           = {self.q3:.4f}")
        print(f"  Maksimum     = {max(self.veri):.4f}")
        print(f"  IQR          = {ceyrekler_arasi_aralik(self.veri):.4f}")
        print(f"  Aykırı Değer = {len(aykiri)} adet: {aykiri[:5]}")
        print(f"{'='*55}")

# ─── DEMO ────────────────────────────────────────────────────────────────────
random.seed(42)

# Normal dağılım benzeri veri + aykırı değerler
veri_normal = [random.gauss(50, 10) for _ in range(200)]
veri_aykiri = veri_normal + [150, -20, 200, -50]  # aykırı değerler ekle

rapor = IstatistikRaporu("Sentetik Veri (n=204)", veri_aykiri)
rapor.rapor_yazdir()

# İki değişken arası korelasyon
x = [random.gauss(50, 10) for _ in range(100)]
y = [xi * 0.7 + random.gauss(0, 5) for xi in x]
print(f"\nPearson r(x,y) = {pearson_r(x, y):.4f}")
