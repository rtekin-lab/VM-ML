# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.7. pyenv ile Çoklu Python Sürüm Yönetimi
# Kitap  : Kod 1.113 (System (set by /home/kullanıcı/.pyenv/versio) · Kod 1.114 (pyenv ile Çoklu Python Sürüm yönetimi) · Kod 1.115 (Dizin bazlı otomatik aktivasyon) · Kod 1.116 (pyenv ile Çoklu Python Sürüm yönetimi) · Kod 1.117 (SÜRÜM DOĞRULAMA)
# Dosya : bolum01/01_04_07_pyenv-ile-coklu-python-surum-yonetimi.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# ─── KURULUM ──────────────────────────────────────────────────────────────────
# macOS (Homebrew)
brew install pyenv pyenv-virtualenv

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# Linux
curl https://pyenv.run | bash

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# ─── PYTHON SÜRÜM YÖNETİMİ ───────────────────────────────────────────────────
pyenv install --list                  # Kurulabilir sürümleri listele
pyenv install 3.11.9                  # Belirli sürümü kur
pyenv install 3.10.14                 # İkinci sürümü kur
pyenv install 3.12.3                  # Üçüncü sürümü kur

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
pyenv versions                        # Kurulu sürümleri göster
# * system (set by /home/kullanici/.pyenv/version)
#   3.10.14
#   3.11.9
#   3.12.3

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
pyenv global 3.11.9                   # Sistem geneli varsayılan
pyenv local  3.10.14                  # Dizin spesifik (.python-version dosyası)
pyenv shell  3.12.3                   # Geçici (mevcut shell oturumu)

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# .python-version dosyası oluşturulur (versiyon kontrolüne ekleyin!)
cat .python-version                   # 3.10.14

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# ─── pyenv-virtualenv ile ENTEGRASYON ────────────────────────────────────────
pyenv virtualenv 3.11.9 ml-proje-311          # Python 3.11 ile sanal ortam
pyenv virtualenv 3.10.14 eski-proje-310       # Python 3.10 ile sanal ortam
pyenv activate ml-proje-311                   # Etkinleştir
pyenv deactivate                              # Devre dışı bırak

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# Dizin bazlı otomatik aktivasyon
cd ~/projeler/ml-proje
pyenv local ml-proje-311             # .python-version'a yaz
# Dizine girildiğinde ortam otomatik aktif olur!

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
pyenv virtualenvs                    # Tüm sanal ortamları listele
pyenv uninstall ml-proje-311         # Ortamı sil

# --- ▌ Kod Örneği 1.4.8 — pyenv ile Çoklu Python Sürüm Yönetimi ---
# ─── SÜRÜM DOĞRULAMA ─────────────────────────────────────────────────────────
python --version                     # Python 3.11.9
python -c "import sys; print(sys.prefix)"  # Ortam yolu
python -c "import sys; print(sys.version_info)"  # Tam sürüm bilgisi
