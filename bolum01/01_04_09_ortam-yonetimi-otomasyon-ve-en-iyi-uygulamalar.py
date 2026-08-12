# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.9. Ortam Yönetimi: Otomasyon ve En İyi Uygulamalar
# Kitap  : Kod 1.121 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.122 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.123 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.124 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.125 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.126 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.127 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.128 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.129 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.130 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.131 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.132 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.133 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.134 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.135 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.136 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.137 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.138 (Ortam Yönetimi: Otomasyon ve En İyi Uygulama) · Kod 1.139 (Kullanım) · Kod 1.140 (Kullanım)
# Dosya : bolum01/01_04_09_ortam-yonetimi-otomasyon-ve-en-iyi-uygulamalar.py
# ==========================================================================
"""
ortam_yonetici.py
Sanal ortam oluşturma, paket kurma ve doğrulama işlemlerini
otomatikleştiren yardımcı araç.
"""
import subprocess
import sys
import os
import json
from pathlib import Path

class OrtamYoneticisi:
    """
    venv tabanlı sanal ortam oluşturucu ve doğrulayıcı.
    Veri bilimi projeleri için optimize edilmiştir.
    """

    ZORUNLU_PAKETLER = {
        'numpy'       : '>=1.24.0',
        'pandas'      : '>=2.0.0',
        'matplotlib'  : '>=3.7.0',
        'scikit-learn': '>=1.3.0',
        'scipy'       : '>=1.11.0',
        'seaborn'     : '>=0.12.0',
        'statsmodels' : '>=0.14.0',
        'jupyterlab'  : '>=4.0.0',
        'ipykernel'   : '>=6.0.0',
    }

    def __init__(self, ortam_adi: str, python_surumu: str = None):
        self.ortam_adi = ortam_adi
        self.ortam_yolu = Path(ortam_adi).resolve()
        self.python_cmd = python_surumu or sys.executable

    def ortam_var_mi(self) -> bool:
        """Sanal ortamın var olup olmadığını kontrol eder."""
        pyvenv_cfg = self.ortam_yolu / 'pyvenv.cfg'
        return pyvenv_cfg.exists()

    def ortam_olustur(self) -> bool:
        """Sanal ortam oluşturur."""
        if self.ortam_var_mi():
            print(f"  ℹ Ortam zaten mevcut: {self.ortam_yolu}")
            return True

        print(f"  → Ortam oluşturuluyor: {self.ortam_adi}")
        sonuc = subprocess.run(
            [self.python_cmd, '-m', 'venv', str(self.ortam_yolu)],
            capture_output=True, text=True
        )
        if sonuc.returncode == 0:
            print(f"  ✓ Ortam oluşturuldu")
            return True
        else:
            print(f"  ✗ Hata: {sonuc.stderr}")
            return False

    def _pip_yolu(self) -> str:
        """OS'a göre pip yolunu döndürür."""
        if sys.platform == 'win32':
            return str(self.ortam_yolu / 'Scripts' / 'pip.exe')
        return str(self.ortam_yolu / 'bin' / 'pip')

    def _python_yolu(self) -> str:
        if sys.platform == 'win32':
            return str(self.ortam_yolu / 'Scripts' / 'python.exe')
        return str(self.ortam_yolu / 'bin' / 'python')

    def pip_guncelle(self):
        """pip'i en güncel sürüme yükseltir."""
        print("  → pip güncelleniyor...")
        subprocess.run([self._pip_yolu(), 'install', '--upgrade', 'pip'],
                       capture_output=True)
        print("  ✓ pip güncellendi")

    def paketleri_yukle(self, paketler: dict = None) -> dict:
        """
        Paketleri yükler ve sonuçları raporlar.
        Returns: {'basarili': [...], 'basarisiz': [...]}
        """
        paketler = paketler or self.ZORUNLU_PAKETLER
        basarili, basarisiz = [], []

        for paket, kisit in paketler.items():
            gereksinim = f"{paket}{kisit}"
            print(f"  → Yükleniyor: {gereksinim}", end=' ', flush=True)
            sonuc = subprocess.run(
                [self._pip_yolu(), 'install', gereksinim],
                capture_output=True, text=True
            )
            if sonuc.returncode == 0:
                print("✓")
                basarili.append(paket)
            else:
                print("✗")
                basarisiz.append(paket)

        return {'basarili': basarili, 'basarisiz': basarisiz}

    def dogrula(self) -> dict:
        """Kurulu paketleri doğrular ve sürüm bilgisi döndürür."""
        dogrulama_kodu = """
import json, importlib
paketler = ['numpy','pandas','matplotlib','scipy','sklearn','statsmodels','seaborn']
sonuclar = {}
for p in paketler:
    try:
        mod = importlib.import_module(p)
        sonuclar[p] = {'durum': 'ok', 'surum': mod.__version__}
    except Exception as e:
        sonuclar[p] = {'durum': 'hata', 'mesaj': str(e)}
print(json.dumps(sonuclar))
"""
        sonuc = subprocess.run(
            [self._python_yolu(), '-c', dogrulama_kodu],
            capture_output=True, text=True
        )
        if sonuc.returncode == 0:
            return json.loads(sonuc.stdout)
        return {}

    def requirements_olustur(self, dosya='requirements.txt'):
        """requirements.txt oluşturur."""
        sonuc = subprocess.run(
            [self._pip_yolu(), 'freeze'],
            capture_output=True, text=True
        )
        with open(dosya, 'w') as f:
            f.write(sonuc.stdout)
        satir_say = len(sonuc.stdout.strip().split('\n'))
        print(f"  ✓ {dosya} oluşturuldu ({satir_say} paket)")

    def tam_kurulum(self):
        """Tüm kurulum adımlarını sırayla çalıştırır."""
        print("=" * 55)
        print(f"  VERİ BİLİMİ ORTAMI KURULUM ARACI")
        print(f"  Ortam: {self.ortam_adi}")
        print("=" * 55)

        adimlar = [
            ("ADIM 1: Ortam Oluşturma", self.ortam_olustur),
            ("ADIM 2: pip Güncelleme",  self.pip_guncelle),
        ]
        for baslik, fonk in adimlar:
            print(f"\n─── {baslik} ───────────────────────")
            fonk()

        print("\n─── ADIM 3: Paket Kurulumu ──────────────────────────")
        sonuc = self.paketleri_yukle()
        print(f"  Başarılı  : {len(sonuc['basarili'])} paket")
        print(f"  Başarısız : {len(sonuc['basarisiz'])} paket")
        if sonuc['basarisiz']:
            print(f"  ✗ Başarısız paketler: {sonuc['basarisiz']}")

        print("\n─── ADIM 4: Doğrulama ───────────────────────────────")
        dogrulama = self.dogrula()
        for paket, bilgi in dogrulama.items():
            durum = '✓' if bilgi['durum'] == 'ok' else '✗'
            bilgi_str = bilgi.get('surum', bilgi.get('mesaj', '?'))
            print(f"  {durum} {paket:<15} {bilgi_str}")

        print("\n─── ADIM 5: requirements.txt ────────────────────────")
        self.requirements_olustur()

        print("\n─── TAMAMLANDI ──────────────────────────────────────")
        etkinlestir = "source" if sys.platform != "win32" else ""
        print(f"  Ortamı etkinleştirmek için:")
        if sys.platform != "win32":
            print(f"  $ source {self.ortam_adi}/bin/activate")
        else:
            print(f"  > .\\{self.ortam_adi}\\Scripts\\activate.bat")
        print("=" * 55)

# Kullanım
if __name__ == '__main__':
    yonetici = OrtamYoneticisi('veri-bilimi-env')
    yonetici.tam_kurulum()
