# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.10. Dosya G/Ç İşlemleri ve Bağlam Yöneticileri
# Kitap  : Kod 1.252 (Dosya G/Ç İşlemleri ve Bağlam Yöneticileri) · Kod 1.253 (Dosya G/Ç İşlemleri ve Bağlam Yöneticileri)
# Dosya : bolum01/01_05_10_dosya-g-c-islemleri-ve-baglam-yoneticileri.py
# ==========================================================================
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import tempfile

import json
import csv
import os
from pathlib import Path
from contextlib import contextmanager

# ─── Temel Dosya G/Ç: McKinney (2022) Ch.3.3 ────────────────────────────────
dosya_yolu = os.path.join(tempfile.gettempdir(), "ornek_veri.txt")

# Yazma (with otomatik kapatır)
with open(dosya_yolu, 'w', encoding='utf-8') as f:
    f.write("Python Veri Bilimi\n")
    f.write("Satır 2\n")
    f.writelines([f"Satır {i}\n" for i in range(3, 8)])

# Okuma modları: 'r' okuma, 'w' yazma, 'a' ekleme, 'rb' ikili okuma
with open(dosya_yolu, 'r', encoding='utf-8') as f:
    satirlar = [satir.rstrip() for satir in f]
print(f"Dosyadan okunan satır sayısı: {len(satirlar)}")
print(f"İlk satır: '{satirlar[0]}'")

# ─── pathlib — Modern Dosya Yolu API'si (Python 3.4+) ────────────────────────
p = Path('/tmp') / 'alt_dizin' / 'dosya.txt'
print(f"\npathlib:")
print(f"  Üst dizin : {p.parent}")
print(f"  Dosya adı : {p.name}")
print(f"  Uzantısız : {p.stem}")
print(f"  Uzantı    : {p.suffix}")

# ─── CSV Okuma/Yazma ──────────────────────────────────────────────────────────
csv_dosyasi = os.path.join(tempfile.gettempdir(), "ogrenciler.csv")
ogrenciler = [
    {'ad': 'Ali',   'soyad': 'Yılmaz', 'not': 85, 'bolum': 'Bilgisayar'},
    {'ad': 'Ayşe',  'soyad': 'Kaya',   'not': 92, 'bolum': 'Matematik'},
    {'ad': 'Mehmet','soyad': 'Demir',  'not': 78, 'bolum': 'Fizik'},
]

# Yazma
with open(csv_dosyasi, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['ad', 'soyad', 'not', 'bolum'])
    writer.writeheader()
    writer.writerows(ogrenciler)

# Okuma
with open(csv_dosyasi, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    okunan = list(reader)
print(f"\nCSV'den okunan öğrenci sayısı: {len(okunan)}")
print(f"Ortalama not: {sum(int(o['not']) for o in okunan)/len(okunan):.2f}")

# ─── JSON Okuma/Yazma ─────────────────────────────────────────────────────────
json_dosyasi = os.path.join(tempfile.gettempdir(), "veri.json")
veri = {
    'proje': 'Veri Madenciliği',
    'versiyon': '1.0',
    'parametreler': {'max_iter': 100, 'tol': 1e-4, 'algoritma': 'k-means'},
    'sonuclar': [0.85, 0.87, 0.91, 0.88]
}

with open(json_dosyasi, 'w', encoding='utf-8') as f:
    json.dump(veri, f, ensure_ascii=False, indent=2)

with open(json_dosyasi, 'r', encoding='utf-8') as f:
    yuklenen = json.load(f)

print(f"\nJSON'dan yüklenen: {yuklenen['proje']} v{yuklenen['versiyon']}")
print(f"Ortalama sonuç: {sum(yuklenen['sonuclar'])/len(yuklenen['sonuclar']):.4f}")

# ─── Özel Bağlam Yöneticisi ──────────────────────────────────────────────────
@contextmanager
def zamanlanmis_islem(islem_adi):
    """İşlem süresini ölçen bağlam yöneticisi."""
    import time
    print(f"⏵ {islem_adi} başlıyor...")
    baslangic = time.perf_counter()
    try:
        yield
    finally:
        sure = time.perf_counter() - baslangic
        print(f"⏹ {islem_adi} tamamlandı ({sure*1000:.2f} ms)")

with zamanlanmis_islem("Büyük Liste Oluşturma"):
    buyuk_liste = list(range(1_000_000))
    toplam = sum(buyuk_liste)
print(f"  Toplam: {toplam:,}")
