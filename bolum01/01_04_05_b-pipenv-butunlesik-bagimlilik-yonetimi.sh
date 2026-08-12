# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.5. virtualenv ve pipenv — Gelişmiş pip Araçları › B. pipenv — Bütünleşik Bağımlılık Yönetimi
# Kitap  : Kod 1.106 (Ortamı tamamen sil)
# Dosya : bolum01/01_04_05_b-pipenv-butunlesik-bagimlilik-yonetimi.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Kurulum
pip install pipenv

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# ─── TEMEL İŞ AKIŞI ───────────────────────────────────────────────────────────
# Proje başlatma (Python sürümü ile)
cd proje-dizini
pipenv --python 3.11              # Yeni ortam + Pipfile oluştur

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Paket yükleme
pipenv install numpy pandas       # Üretim bağımlılıkları → Pipfile [packages]
pipenv install pytest --dev       # Geliştirme bağımlılıkları → [dev-packages]

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Ortamı etkinleştir
pipenv shell                      # Ortam kabuğuna gir
exit                              # Kabuktan çık

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Tek komutla çalıştır (etkinleştirme olmadan)
pipenv run python script.py
pipenv run jupyter lab

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Pipfile.lock oluştur (deterministik kurulum)
pipenv lock

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Başka makinede tam ortamı yeniden oluştur
pipenv install --ignore-pipfile   # Pipfile.lock'tan

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# requirements.txt'ten geçiş
pipenv install -r requirements.txt

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Güvenlik açığı taraması
pipenv check

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Bağımlılık grafiğini görselleştir
pipenv graph
# pandas==2.2.1
#   - numpy [required: >=1.23.5, installed: 1.26.4]
#   - python-dateutil [required: >=2.8.2, installed: 2.9.0]
#   - pytz [required: >=2020.1, installed: 2024.1]

# --- ▌ Kod Örneği 1.4.6 — pipenv Kapsamlı Kullanım ---
# Ortamı tamamen sil
pipenv --rm
