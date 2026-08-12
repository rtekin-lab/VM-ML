#!/usr/bin/env python3
"""
Python 3.12 öncesi sürümlerde hata veren f-string kalıplarını bulur ve onarır.

PEP 701 (Python 3.12) ile birlikte bir f-string'in içindeki ifade kısmında
dış tırnakla AYNI tırnağı kullanmak serbest bırakıldı:

    f'{sozluk['anahtar']}'      # 3.12+ geçerli, 3.11 ve öncesinde SyntaxError
    f'{metin.split('\\n')[0]}'   # aynı şekilde

Bu betik iç tırnakları ters tipe çevirerek kodu 3.8+ ile uyumlu hâle getirir:

    f'{sozluk["anahtar"]}'

Ayrıca 3.12 öncesinde yasak olan "ifade içinde ters bölü" durumlarını raporlar.

Kullanım:
    python kod/arac/fstring_uyumlu_yap.py --kod ./kod --onizleme
    python kod/arac/fstring_uyumlu_yap.py --kod ./kod
"""
import argparse
import re
import sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
ONEK = re.compile(r'([fF][rRbB]?|[rRbB][fF])$')


def fstring_tara(satir):
    """Satırdaki f-string'leri gez; ifade kısmında dış tırnak varsa konumlarını döndür."""
    duzeltmeler = []          # (indeks, yeni_karakter)
    ters_boluk = False
    i = 0
    n = len(satir)
    while i < n:
        ch = satir[i]
        if ch in '\'"':
            # önek kontrolü: f / rf / fr ...
            j = i
            k = i - 1
            onek = ''
            while k >= 0 and satir[k].isalpha():
                onek = satir[k] + onek
                k -= 1
            fmi = bool(ONEK.match(onek)) if onek else False
            tirnak = ch
            uclu = satir.startswith(tirnak * 3, i)
            kapanis = tirnak * (3 if uclu else 1)
            i += len(kapanis)
            derinlik = 0
            while i < n:
                c = satir[i]
                if c == '\\':
                    if fmi and derinlik > 0:
                        ters_boluk = True
                    i += 2
                    continue
                if fmi and c == '{':
                    if satir.startswith('{{', i):
                        i += 2
                        continue
                    derinlik += 1
                    i += 1
                    continue
                if fmi and c == '}':
                    if satir.startswith('}}', i) and derinlik == 0:
                        i += 2
                        continue
                    derinlik = max(derinlik - 1, 0)
                    i += 1
                    continue
                if c == tirnak:
                    if derinlik > 0:
                        # ifade içinde dış tırnakla aynı tırnak → çevir
                        duzeltmeler.append(i)
                        i += 1
                        continue
                    if satir.startswith(kapanis, i):
                        i += len(kapanis)
                        break
                i += 1
            continue
        i += 1
    return duzeltmeler, ters_boluk


def satiri_onar(satir):
    yerler, tb = fstring_tara(satir)
    if not yerler:
        return satir, 0, tb
    s = list(satir)
    for idx in yerler:
        s[idx] = '"' if s[idx] == "'" else "'"
    return ''.join(s), len(yerler), tb


ap = argparse.ArgumentParser()
ap.add_argument('--kod', type=Path, default=BURASI.parent)
ap.add_argument('--onizleme', action='store_true')
A = ap.parse_args()

KOD = A.kod.resolve()
dosyalar = sorted(KOD.glob('bolum*/*.py'))
if not dosyalar:
    sys.exit(f'HATA: {KOD} altında .py yok. --kod ile doğru klasörü verin.')

top_dosya = top_satir = 0
uyari = []
for y in dosyalar:
    ham = y.read_text(encoding='utf-8')
    yeni_satirlar, degisti = [], 0
    for no, satir in enumerate(ham.split('\n'), 1):
        yeni, adet, tb = satiri_onar(satir)
        if adet:
            degisti += adet
            if len(uyari) < 12:
                uyari.append(f'  {y.parent.name}/{y.name}:{no}\n'
                             f'      önce : {satir.strip()[:88]}\n'
                             f'      sonra: {yeni.strip()[:88]}')
        if tb:
            uyari.append(f'  ! {y.parent.name}/{y.name}:{no} '
                         f'ifade içinde ters bölü (3.12 öncesi desteklemez)')
        yeni_satirlar.append(yeni)
    if degisti:
        top_dosya += 1
        top_satir += degisti
        if not A.onizleme:
            import ast
            metin = '\n'.join(yeni_satirlar)
            try:
                ast.parse(metin)
            except SyntaxError as e:
                print(f'ATLANDI (onarım sonrası hata): {y.name} — {e.msg}')
                continue
            y.write_text(metin, encoding='utf-8')

print(f'{len(dosyalar)} dosya tarandı')
print(f'{top_dosya} dosyada {top_satir} f-string düzeltildi'
      + (' (ÖNİZLEME — değişiklik yazılmadı)' if A.onizleme else ''))
if uyari:
    print('\nÖrnekler:')
    print('\n'.join(uyari[:12]))
