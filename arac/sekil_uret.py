#!/usr/bin/env python3
"""
Kitaptaki kod dosyalarını çalıştırıp ürettikleri grafikleri PNG olarak kaydeder.

Kullanım
--------
    python kod/arac/sekil_uret.py                # yolları kendisi bulur
    python kod/arac/sekil_uret.py --liste        # çalıştırmaz, planı gösterir
    python kod/arac/sekil_uret.py --bolum 4      # yalnızca 4. bölüm
    python kod/arac/sekil_uret.py --kod ./kod --cikti ./sekiller

Varsayılan yollar betiğin kendi konumuna göre bulunur:
    <depo>/kod/arac/sekil_uret.py  →  kod: <depo>/kod   çıktı: <depo>/sekiller
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

BURASI = Path(__file__).resolve().parent


def varsayilan_kod():
    for a in (BURASI.parent, Path.cwd() / 'kod', Path.cwd()):
        if a.is_dir() and any(a.glob('bolum*')):
            return a.resolve()
    return BURASI.parent.resolve()


ap = argparse.ArgumentParser()
ap.add_argument('--kod', type=Path, default=None, help='kod/ klasörü')
ap.add_argument('--cikti', type=Path, default=None, help='PNG çıktı klasörü')
ap.add_argument('--bolum', type=int, default=None, help='yalnızca bu bölüm (1-13)')
ap.add_argument('--zaman-asimi', type=int, default=90, dest='zaman',
                help='dosya başına saniye (varsayılan 90)')
ap.add_argument('--liste', action='store_true', help='çalıştırma, planı göster')
ap.add_argument('--temizle', action='store_true', help='çıktı klasörünü baştan oluştur')
ap.add_argument('--denetle', action='store_true',
                help='kod dosyalarının güncel sürüm olup olmadığını denetle')
A = ap.parse_args()

KOD = (A.kod or varsayilan_kod()).resolve()
CIKTI = (A.cikti or KOD.parent / 'sekiller').resolve()

if not KOD.is_dir():
    sys.exit(f'HATA: kod klasörü bulunamadı: {KOD}\n'
             f'      --kod ile elle verin, örn:  --kod ./kod')

desen = f'bolum{A.bolum:02d}/*.py' if A.bolum else 'bolum*/*.py'
dosyalar = sorted(KOD.glob(desen))
if not dosyalar:
    icerik = sorted(p.name for p in KOD.iterdir())[:10]
    sys.exit(f'HATA: {KOD} altında .py dosyası yok (aranan: {desen}).\n'
             f'      Beklenen yapı : {KOD}/bolum01/*.py\n'
             f'      Bu klasörde   : {icerik}\n'
             f'      Doğru klasörü --kod ile verin.')

print(f'kod klasörü : {KOD}')
print(f'çıktı       : {CIKTI}')
print(f'dosya       : {len(dosyalar)}\n')


def kurulu_mu(ad):
    try:
        return importlib.util.find_spec(ad) is not None
    except Exception:                                          # noqa: BLE001
        return False


IC = set(getattr(sys, 'stdlib_module_names', ()))
IMP = re.compile(r'^\s*(?:import|from)\s+([A-Za-z_][\w]*)', re.M)

gerekli = set()
for y in dosyalar:
    gerekli |= set(IMP.findall(y.read_text(encoding='utf-8', errors='ignore')))
gerekli -= IC
EKSIK = {m for m in gerekli if not kurulu_mu(m)}

if EKSIK:
    print('Kurulu OLMAYAN kütüphaneler — bunları kullanan dosyalar atlanacak:')
    print('  ' + ', '.join(sorted(EKSIK)))
    print('  Kurmak için: pip install -r kod/arac/requirements-sekil.txt\n')
else:
    print('Gereken tüm kütüphaneler kurulu.\n')

SABLON = '''
import sys
# Windows konsolu varsayilan olarak cp1254 kullanir; kodlardaki ≥, →, ↔ gibi
# karakterler UnicodeEncodeError verir. Cikti akislarini UTF-8'e zorla.
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as _plt
import warnings, os, builtins
warnings.filterwarnings("ignore")
_plt.rcParams["figure.dpi"] = 110
_plt.rcParams["savefig.dpi"] = 150
_plt.rcParams["font.size"] = 9
_N = [0]
_HEDEF = {hedef!r}
_ADI = {adi!r}

def _kaydet():
    for num in _plt.get_fignums():
        fig = _plt.figure(num)
        if not fig.get_axes():
            continue
        _N[0] += 1
        fig.savefig(os.path.join(_HEDEF, "%s__%02d.png" % (_ADI, _N[0])),
                    bbox_inches="tight", facecolor="white")
    _plt.close("all")

_plt.show = lambda *a, **k: _kaydet()
builtins.input = lambda *a, **k: ""

try:
    _src = open({dosya!r}, encoding="utf-8").read()
    exec(compile(_src, {dosya!r}, "exec"),
         {{"__name__": "__main__", "__file__": {dosya!r}}})
finally:
    _kaydet()
'''

if A.denetle:
    IZLER = [
        ('bolum10/10_02_01', 'self.sabir',            'Perceptron ogrenme egrisi'),
        ('bolum07/07_02_02', 'max_iter=1000',         't-SNE (sklearn 1.7 uyumu)'),
        ('bolum07/07_01_03_python', '"eps": 0.35',    'DBSCAN halkalar'),
        ('bolum07/07_01_02', 'X_anz_sc',              'Baglanti olcutu karsilastirmasi'),
        ('bolum07/07_01_01', 'plt.get_cmap("tab10")', 'Silhouette (matplotlib 3.11)'),
        ('bolum10/10_04_02', 'set_visible(False)',    'Aktivasyon bos panel'),
        ('bolum04/04_02_04_03', '"color":"#3498db"',  'regplot renk cakismasi'),
        ('bolum04/04_02_05_01', '.astype(int)',       'heatmap fmt=d'),
        ('bolum04/04_01_09', "resample('ME')",        'pandas 2.2 frekans'),
        ('bolum12/12_02_03', 'GERCEK OLCUM',          'MapReduce gercek olcum'),
        ('bolum03/03_02_06_02', 'olcekler = torch',   'BatchNorm tasma'),
        ('bolum01/01_04_03_b', 'importlib.metadata',  'pkg_resources'),
    ]
    eksik = 0
    print('Dosya guncellik denetimi')
    print('-' * 62)
    for onek, iz, ad in IZLER:
        adaylar = [q for q in KOD.glob(onek + '*') if q.suffix in ('.py', '.ipy')]
        var = any(iz in q.read_text(encoding='utf-8', errors='ignore') for q in adaylar)
        if not var:
            eksik += 1
        print(f'  {"OK " if var else "ESKI"}  {ad}')
    print('-' * 62)
    if eksik:
        print(f'{eksik} dosya ESKI surumde. kod/ klasorunu tamamen silip zip\'i')
        print('yeniden acin (uzerine yazmak Dropbox/Drive senkronunda yetmeyebilir).')
    else:
        print('Tum dosyalar guncel.')
    sys.exit(1 if eksik else 0)

if A.liste:
    for y in dosyalar:
        kul = set(IMP.findall(y.read_text(encoding='utf-8', errors='ignore')))
        eks = sorted(kul & EKSIK)
        print(f'  {y.parent.name}/{y.name[:58]:<58} '
              f'{"ATLANIR: " + ", ".join(eks) if eks else "çalıştırılır"}')
    sys.exit(0)

if A.temizle and CIKTI.exists():
    shutil.rmtree(CIKTI)
CIKTI.mkdir(parents=True, exist_ok=True)

sonuc = []
gecici = Path(tempfile.mkdtemp(prefix='vmml_'))
kosucu = gecici / '_kosucu.py'

for i, y in enumerate(dosyalar, 1):
    rel = f'{y.parent.name}/{y.name}'
    adi = f'{y.parent.name}__{y.stem}'
    metin = y.read_text(encoding='utf-8', errors='ignore')

    eks = sorted(set(IMP.findall(metin)) & EKSIK)
    if eks:
        sonuc.append(dict(dosya=rel, durum='atlandi', neden=', '.join(eks)))
        continue
    if 'matplotlib' not in metin and 'seaborn' not in metin:
        sonuc.append(dict(dosya=rel, durum='grafik-yok'))
        continue

    kosucu.write_text(SABLON.format(hedef=str(CIKTI), adi=adi, dosya=str(y)),
                      encoding='utf-8')
    print(f'[{i}/{len(dosyalar)}] {rel} … ', end='', flush=True)
    try:
        ortam = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
        r = subprocess.run([sys.executable, str(kosucu)], capture_output=True,
                           timeout=A.zaman, text=True, encoding='utf-8',
                           errors='replace', cwd=str(gecici), env=ortam)
        urun = sorted(CIKTI.glob(f'{adi}__*.png'))
        if urun:
            print(f'{len(urun)} şekil')
            sonuc.append(dict(dosya=rel, durum='ok', sekil=len(urun),
                              dosyalar=[p.name for p in urun]))
        else:
            satirlar = [l for l in (r.stderr or '').strip().split('\n')
                        if l.strip() and not l.lstrip().startswith(('20', 'W', 'I', '2026-'))
                        and 'oneDNN' not in l and 'AVX2' not in l and 'TF-TRT' not in l]
            hata = (satirlar[-1] if satirlar else '')[:120]
            print('şekil yok' + (f' — {hata}' if hata else ''))
            sonuc.append(dict(dosya=rel, durum='sekil-yok', hata=hata))
    except subprocess.TimeoutExpired:
        print('zaman aşımı')
        sonuc.append(dict(dosya=rel, durum='zaman-asimi'))
    except Exception as e:                                     # noqa: BLE001
        print(f'hata: {e}')
        sonuc.append(dict(dosya=rel, durum='hata', hata=str(e)[:120]))

shutil.rmtree(gecici, ignore_errors=True)

rapor = CIKTI.parent / 'sekil_sonuc.json'
rapor.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding='utf-8')

print('\n' + '-' * 52)
for k, v in Counter(s['durum'] for s in sonuc).most_common():
    print(f'  {k:<12} {v}')
print(f'  {"ŞEKİL":<12} {sum(s.get("sekil", 0) for s in sonuc)}')
print(f'\nPNG klasörü : {CIKTI}')
print(f'Rapor       : {rapor}')
print('\nSonraki adım: sekiller/ klasörünü açıp boş, okunaksız ve tekrarlı')
print('grafikleri SİLİN, ardından sekil_yerlestir.py çalıştırın.')
