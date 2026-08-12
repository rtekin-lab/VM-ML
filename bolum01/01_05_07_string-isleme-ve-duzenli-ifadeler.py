# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.5. Temel Python Konuları › 1.5.7. String İşleme ve Düzenli İfadeler
# Kitap  : Kod 1.214 (Birleştirme) · Kod 1.215 (F-string İleri Formatlama) · Kod 1.216 (Düzenli İfadeler (re modülü)) · Kod 1.217 (E-posta doğrulama) · Kod 1.218 (Grup yakalama) · Kod 1.219 (Re.sub ile desen değiştirme (veri temizleme)) · Kod 1.220 (Re.sub ile desen değiştirme (veri temizleme))
# Dosya : bolum01/01_05_07_string-isleme-ve-duzenli-ifadeler.py
# ==========================================================================
import re
import unicodedata

# ─── String Metodları: McKinney (2022) Ch.7.3 ────────────────────────────────
metin = "  Python Veri Bilimi ve Makine Öğrenmesi  "

print("─── Temel Metodlar ────────────────────────────────────────")
print(f"strip()    : '{metin.strip()}'")
print(f"lower()    : '{metin.strip().lower()}'")
print(f"upper()    : '{metin.strip().upper()}'")
print(f"title()    : '{metin.strip().title()}'")
print(f"replace()  : '{metin.strip().replace('ve', '&')}'")
print(f"split()    : {metin.strip().split()}")
print(f"count('i') : {metin.count('i')}")
print(f"find('Veri'): {metin.find('Veri')}")
print(f"startswith: {metin.strip().startswith('Python')}")

# Birleştirme
kelimeler = ['Python', 'Veri', 'Bilimi']
print(f"' '.join(): '{' '.join(kelimeler)}'")
print(f"'-'.join(): '{'-'.join(kelimeler)}'")

# ─── f-string İleri Formatlama ────────────────────────────────────────────────
pi, e = 3.14159265358979, 2.71828182845904
veri = {'isim': 'Ahmet', 'puan': 98.7654}

print("\n─── f-string Formatlama ────────────────────────────────────")
print(f"Pi     : {pi:.4f}")           # 4 ondalık
print(f"Pi %   : {pi:10.4f}")         # sağa hizalı, genişlik 10
print(f"Bilimsel: {pi:e}")            # bilimsel gösterim
print(f"Yüzde  : {0.8534:.1%}")       # yüzde formatı
print(f"Ondalık: {12345678:,}")       # binlik ayraç
print(f"Hex    : {255:#010x}")        # hex, 10 karakter
print(f"Hizalı : {veri['isim']:<10}{veri['puan']:>8.2f}")

# ─── Düzenli İfadeler (re modülü) ────────────────────────────────────────────
print("\n─── Düzenli İfadeler (Regex) ────────────────────────────────")

# Temel desenler
metin = "Ahmet 0532-555-1234, Veli 0212 333 44 55, Ayşe: +90-216-777-8888"

# Telefon numaralarını bul
tel_desen = r'\+?\d[\d\s\-]{7,}'
telefonlar = re.findall(tel_desen, metin)
print(f"Telefonlar: {telefonlar}")

# E-posta doğrulama
email_desen = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
emailler = ['kullanici@ornek.com', 'gecersiz@', 'diger@test.org', 'hata']
for email in emailler:
    gecerli = bool(re.match(email_desen, email))
    print(f"  {email:<30}: {'✓ Geçerli' if gecerli else '✗ Geçersiz'}")

# Grup yakalama
log_desen = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)'
log_satiri = '2024-03-15 14:23:07 [ERROR] Bağlantı zaman aşımına uğradı'
eslesme = re.match(log_desen, log_satiri)
if eslesme:
    tarih, saat, seviye, mesaj = eslesme.groups()
    print(f"\nLog analizi:")
    print(f"  Tarih  : {tarih}")
    print(f"  Saat   : {saat}")
    print(f"  Seviye : {seviye}")
    print(f"  Mesaj  : {mesaj}")

# re.sub ile desen değiştirme (veri temizleme)
kirli_veri = "Fiyat:   1.234,56 TL  (KDV dahil)"
temiz = re.sub(r'[^\d,]', '', kirli_veri)
print(f"\nVeri temizleme: '{kirli_veri}' → '{temiz}'")
