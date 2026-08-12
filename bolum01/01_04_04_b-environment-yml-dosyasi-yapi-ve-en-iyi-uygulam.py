# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.4. conda ile Ortam Yönetimi › B. environment.yml Dosyası: Yapı ve En İyi Uygulamalar
# Kitap  : Kod 1.96 (Environment.yml oluşturma ve doğrulama scrip) · Kod 1.97 (Environment.yml Dosyası: Yapı ve En İyi Uygu) · Kod 1.98 (Environment.yml Dosyası: Yapı ve En İyi Uygu) · Kod 1.99 (Kullanım) · Kod 1.100 (Kullanım)
# Dosya : bolum01/01_04_04_b-environment-yml-dosyasi-yapi-ve-en-iyi-uygulam.py
# ==========================================================================
# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
# ─── Üretim Kalitesinde environment.yml Örneği ────────────────────────────────
# Bu dosyayı projenizin kök dizinine koyun ve versiyon kontrolüne ekleyin

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
# Dosya adı: environment.yml
#
# name: veri-madenciligi-projesi
# channels:
#   - conda-forge        # Birincil kanal — daha güncel ikili paketler
#   - defaults           # Fallback kanal
# dependencies:
#   - python=3.11        # Python sürümünü sabitleyin
#   - numpy=1.26.4       # Kritik paketlerde tam sürüm sabitleme
#   - pandas=2.2.1
#   - matplotlib=3.9.0
#   - scikit-learn=1.5.0
#   - scipy=1.13.0
#   - statsmodels=0.14.2
#   - jupyterlab=4.2.0
#   - seaborn=0.13.2
#   - ipykernel          # Jupyter kernel kaydı için
#   - pip:               # conda'da olmayan paketler için
#     - missingno==0.5.2
#     - yfinance==0.2.38
#
# Kullanım:
#   conda env create -f environment.yml
#   conda activate veri-madenciligi-projesi

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
# ─── environment.yml oluşturma ve doğrulama scripti ──────────────────────────
import subprocess
import json

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
def ortam_olustur(env_name, python_ver='3.11'):
    """Conda ortamı oluşturup doğrular."""
    print(f"Ortam oluşturuluyor: {env_name} (Python {python_ver})")

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
    cmd = ['conda', 'create', '-y', '-n', env_name, f'python={python_ver}']
    sonuc = subprocess.run(cmd, capture_output=True, text=True)

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
    if sonuc.returncode == 0:
        print(f"  ✓ Ortam başarıyla oluşturuldu")
    else:
        print(f"  ✗ Hata: {sonuc.stderr[:200]}")
        return False
    return True

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
def environment_yml_olustur(env_name, cikti_yolu='environment.yml'):
    """Mevcut ortamdan environment.yml üretir."""
    cmd = ['conda', 'env', 'export', '-n', env_name]
    sonuc = subprocess.run(cmd, capture_output=True, text=True)

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
    if sonuc.returncode == 0:
        with open(cikti_yolu, 'w', encoding='utf-8') as f:
            f.write(sonuc.stdout)
        print(f"  ✓ {cikti_yolu} oluşturuldu ({len(sonuc.stdout)} karakter)")
    else:
        print(f"  ✗ Dışa aktarma hatası")

# --- ▌ Kod Örneği 1.4.4 — Üretim Kalitesinde environment.yml ---
# Kullanım
# ortam_olustur("test-env", "3.11")
# environment_yml_olustur("test-env")
print("environment.yml yönetim fonksiyonları hazır.")
