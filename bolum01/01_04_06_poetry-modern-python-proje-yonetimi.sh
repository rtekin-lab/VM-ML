# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.6. Poetry — Modern Python Proje Yönetimi
# Kitap  : Kod 1.108 (ORTAM VE ÇALIŞTIRMA) · Kod 1.109 (POETRY.LOCK) · Kod 1.110 (PAKET YAYIMLAMA) · Kod 1.111 (PAKET YAYIMLAMA)
# Dosya : bolum01/01_04_06_poetry-modern-python-proje-yonetimi.sh
# ==========================================================================
# Kurulum (pip dışı yöntem önerilir)
curl -sSL https://install.python-poetry.org | python3 -
# veya: pip install poetry

# ─── PROJE OLUŞTURMA ─────────────────────────────────────────────────────────
poetry new veri-madenciligi-projesi        # Yeni proje oluştur
cd veri-madenciligi-projesi

# Mevcut dizinde başlat
poetry init                                # Etkileşimli yapılandırma

# ─── PAKET YÖNETİMİ ──────────────────────────────────────────────────────────
poetry add numpy pandas scikit-learn       # Üretim bağımlılıkları
poetry add pytest black --group dev        # Geliştirme bağımlılıkları
poetry add "scikit-learn>=1.3,<2.0"        # Sürüm aralığı ile ekleme
poetry remove numpy                        # Paket kaldır
poetry update                             # Tüm paketleri güncelle

# ─── ORTAM VE ÇALIŞTIRMA ─────────────────────────────────────────────────────
poetry install                            # Ortamı kur (poetry.lock'tan)
poetry shell                              # Ortama gir
poetry run python script.py               # Ortamda çalıştır
poetry run jupyter lab                    # Jupyter başlat
poetry env info                           # Ortam bilgisi
poetry env list                           # Tüm ortamları listele

# ─── POETRY.LOCK ─────────────────────────────────────────────────────────────
# poetry.lock, Pipfile.lock gibi tam bağımlılık çözümünü saklar
# Git'e eklenmeli! → .gitignore'a EKLEME
poetry lock                               # lock dosyasını yenile
poetry install --no-dev                   # Sadece üretim bağımlılıkları

# ─── PAKET YAYIMLAMA ─────────────────────────────────────────────────────────
poetry build                              # sdist ve wheel oluştur
poetry publish                            # PyPI'ye yayımla
poetry publish --repository testpypi      # Test PyPI'ye yayımla
