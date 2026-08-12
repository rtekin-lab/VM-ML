# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.11. Tip İpuçları ve Veri Doğrulama
# Kitap  : Kod 1.254 (Tip İpuçları ve Veri doğrulama) · Kod 1.255 (Tip İpuçları ve Veri doğrulama) · Kod 1.256 (Tip İpuçları ve Veri doğrulama) · Kod 1.257 (Tip İpuçları ve Veri doğrulama) · Kod 1.258 (Tip İpuçları ve Veri doğrulama) · Kod 1.259 (Tip İpuçları ve Veri doğrulama) · Kod 1.260 (Str yığını (aynı sınıf, farklı tıp)) · Kod 1.261 (Str yığını (aynı sınıf, farklı tıp))
# Dosya : bolum01/01_05_11_tip-ipuclari-ve-veri-dogrulama.py
# ==========================================================================
from typing import (List, Dict, Tuple, Optional, Union,
                    Callable, TypeVar, Generic, Any)
from functools import wraps

T = TypeVar('T')  # Jenerik tip parametresi

# ─── Temel Tip İpuçları ───────────────────────────────────────────────────────
def vektör_dot_çarpım(v1: List[float], v2: List[float]) -> float:
    """
    Vektör iç çarpımı: ⟨v1, v2⟩ = Σ v1_i * v2_i
    Grus (2015): "İki vektörün dot çarpımı bileşensel çarpımlarının toplamıdır"
    """
    if len(v1) != len(v2):
        raise ValueError(f"Boyut uyumsuzluğu: {len(v1)} ≠ {len(v2)}")
    return sum(a * b for a, b in zip(v1, v2))

def vektör_normalize(v: List[float]) -> List[float]:
    """Birim vektöre normalize et: v̂ = v / ‖v‖"""
    norm = sum(x**2 for x in v) ** 0.5
    if norm == 0:
        raise ValueError("Sıfır vektörü normalize edilemez")
    return [x / norm for x in v]

v1 = [1.0, 2.0, 3.0]
v2 = [4.0, 5.0, 6.0]
print(f"v1 · v2 = {vektör_dot_çarpım(v1, v2)}")   # 1*4 + 2*5 + 3*6 = 32
print(f"‖v1‖ = {sum(x**2 for x in v1)**0.5:.4f}")

v1_hat = vektör_normalize(v1)
print(f"v̂1 = {[f'{x:.4f}' for x in v1_hat]}")
print(f"‖v̂1‖ = {sum(x**2 for x in v1_hat)**0.5:.6f}")  # ≈ 1.0

# ─── Optional ve Union ────────────────────────────────────────────────────────
def güvenli_bölme(pay: Union[int, float],
                  payda: Union[int, float]) -> Optional[float]:
    """None döndürür: sıfıra bölme durumunda."""
    if payda == 0:
        return None
    return pay / payda

sonuç = güvenli_bölme(10, 3)
if sonuç is not None:
    print(f"\n10/3 = {sonuç:.4f}")

# ─── Jenerik Sınıf ───────────────────────────────────────────────────────────
class İstifle(Generic[T]):
    """Jenerik yığın (stack) veri yapısı — LIFO."""
    def __init__(self):
        self._veri: List[T] = []

    def ekle(self, eleman: T) -> None:
        self._veri.append(eleman)

    def çıkar(self) -> T:
        if not self._veri:
            raise IndexError("Boş yığından çıkarma!")
        return self._veri.pop()

    def tepe(self) -> Optional[T]:
        return self._veri[-1] if self._veri else None

    def __len__(self) -> int:
        return len(self._veri)

    def __repr__(self) -> str:
        return f"İstifle({self._veri})"

# int yığını
int_istif: İstifle[int] = İstifle()
for i in [1, 2, 3, 4, 5]:
    int_istif.ekle(i)
print(f"\nYığın: {int_istif}")
print(f"Tepe: {int_istif.tepe()}")
print(f"Çıkarılan: {int_istif.çıkar()}")

# str yığını (aynı sınıf, farklı tip)
str_istif: İstifle[str] = İstifle()
for kelime in ["Python", "Veri", "Bilimi"]:
    str_istif.ekle(kelime)
print(f"String yığın: {str_istif}")
