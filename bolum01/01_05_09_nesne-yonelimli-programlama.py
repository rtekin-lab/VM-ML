# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.9. Nesne Yönelimli Programlama (OOP)
# Kitap  : Kod 1.230 (Temel Sınıf Tanımı) · Kod 1.231 (Örnek değişkenleri) · Kod 1.232 (Sihirli Metodlar (Dunder Methods)) · Kod 1.233 (Nesne Yönelimli Programlama (OOP)) · Kod 1.234 (Statik metod) · Kod 1.235 (Kalıtım ve Polimorfizm) · Kod 1.236 (Nesne Yönelimli Programlama (OOP)) · Kod 1.237 (Nesne Yönelimli Programlama (OOP)) · Kod 1.238 (Nesne Yönelimli Programlama (OOP)) · Kod 1.239 (Nesne Yönelimli Programlama (OOP)) · Kod 1.240 (Polimorfizm: Aynı arayüz, farklı davranış) · Kod 1.241 (Nesne Yönelimli Programlama (OOP)) · Kod 1.242 (Nesne Yönelimli Programlama (OOP)) · Kod 1.243 (Nesne Yönelimli Programlama (OOP))
# Dosya : bolum01/01_05_09_nesne-yonelimli-programlama.py
# ==========================================================================
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import math
from typing import List, Optional

# ─── Temel Sınıf Tanımı ───────────────────────────────────────────────────────
class VeriNoktasi:
    """
    Temel veri noktası sınıfı.
    Kapsülleme: veriler __init__ içinde tanımlanır.
    """
    # Sınıf değişkeni: tüm örnekler tarafından paylaşılır
    toplam_nokta = 0

    def __init__(self, x: float, y: float, etiket: str = ""):
        # Örnek değişkenleri
        self.x = x
        self.y = y
        self.etiket = etiket
        VeriNoktasi.toplam_nokta += 1

    # Sihirli Metodlar (Dunder Methods)
    def __repr__(self):
        return f"VeriNoktasi(x={self.x}, y={self.y}, etiket='{self.etiket}')"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, diger):
        return VeriNoktasi(self.x + diger.x, self.y + diger.y)

    def __eq__(self, diger):
        if not isinstance(diger, VeriNoktasi): return NotImplemented
        return self.x == diger.x and self.y == diger.y

    def __lt__(self, diger):
        return self.uzaklik_orijin() < diger.uzaklik_orijin()

    def __len__(self):  # Sözde boyut (2B nokta)
        return 2

    # Örnek metodu
    def uzaklik_orijin(self) -> float:
        """Öklid uzaklığı: d = √(x² + y²)"""
        return math.sqrt(self.x**2 + self.y**2)

    def uzaklik(self, diger: 'VeriNoktasi') -> float:
        """İki nokta arası Öklid uzaklığı."""
        return math.sqrt((self.x - diger.x)**2 + (self.y - diger.y)**2)

    # Sınıf metodu
    @classmethod
    def orijin(cls) -> 'VeriNoktasi':
        """Fabrika metodu: (0,0) noktası."""
        return cls(0.0, 0.0, "Orijin")

    # Statik metod
    @staticmethod
    def kosul_dogrula(x, y) -> bool:
        return isinstance(x, (int, float)) and isinstance(y, (int, float))

# ─── Kalıtım ve Polimorfizm ───────────────────────────────────────────────────
class Sekil(ABC):
    """Soyut temel sınıf — abstractmethod ile zorunlu arayüz."""
    def __init__(self, renk: str = "siyah"):
        self.renk = renk

    @abstractmethod
    def alan(self) -> float: ...

    @abstractmethod
    def cevre(self) -> float: ...

    def tanim(self) -> str:
        return f"{type(self).__name__}(renk={self.renk}, alan={self.alan():.4f})"

class Daire(Sekil):
    def __init__(self, yaricap: float, renk: str = "siyah"):
        super().__init__(renk)
        self.yaricap = yaricap

    def alan(self) -> float:    return math.pi * self.yaricap ** 2
    def cevre(self) -> float:   return 2 * math.pi * self.yaricap

class Dikdortgen(Sekil):
    def __init__(self, en: float, boy: float, renk: str = "siyah"):
        super().__init__(renk)
        self.en = en; self.boy = boy

    def alan(self) -> float:    return self.en * self.boy
    def cevre(self) -> float:   return 2 * (self.en + self.boy)

class Ucgen(Sekil):
    def __init__(self, a: float, b: float, c: float, renk: str = "siyah"):
        super().__init__(renk)
        self.a = a; self.b = b; self.c = c

    def alan(self) -> float:    # Heron formülü: A = √(s(s-a)(s-b)(s-c))
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s*(s-self.a)*(s-self.b)*(s-self.c))
    def cevre(self) -> float:   return self.a + self.b + self.c

# ─── Polimorfizm: Aynı arayüz, farklı davranış ────────────────────────────────
print("─── Polimorfizm: Sekil Hiyerarşisi ─────────────────────────")
sekiller = [Daire(5), Dikdortgen(4, 6), Ucgen(3, 4, 5), Daire(2.5, "kırmızı")]

for sekil in sekiller:
    print(f"  {sekil.tanim():<50}  Çevre={sekil.cevre():.4f}")

toplam_alan = sum(s.alan() for s in sekiller)
print(f"Toplam alan: {toplam_alan:.4f}")

# ─── @dataclass (Python 3.7+) ────────────────────────────────────────────────
@dataclass(order=True)
class IstatistikOzeti:
    """Veri sınıfı: __init__, __repr__, __eq__, __lt__ otomatik üretilir."""
    sort_index: float = field(init=False, repr=False)  # sıralama için
    veri_adi: str
    n: int
    ortalama: float
    std: float
    minimum: float
    maksimum: float

    def __post_init__(self):
        self.sort_index = self.ortalama

    @property
    def aralik(self) -> float:
        return self.maksimum - self.minimum

    @property
    def gucendirme_katsayisi(self) -> float:
        """CV = σ/μ — değişkenlik katsayısı"""
        return (self.std / self.ortalama) if self.ortalama != 0 else float('inf')

import random
random.seed(42)
veri = [random.gauss(50, 10) for _ in range(100)]

ozet = IstatistikOzeti(
    veri_adi="Örnek Veri",
    n=len(veri),
    ortalama=sum(veri)/len(veri),
    std=math.sqrt(sum((x - sum(veri)/len(veri))**2 for x in veri)/len(veri)),
    minimum=min(veri),
    maksimum=max(veri)
)
print(f"\n─── Veri Sınıfı (dataclass) ─────────────────────────────")
print(f"{ozet}")
print(f"Aralık : {ozet.aralik:.4f}")
print(f"CV     : {ozet.gucendirme_katsayisi:.4f}")
