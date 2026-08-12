# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.1. Paket Yöneticileri: pip ve conda › A. pip — Python'ın Standart Paket Yöneticisi
# Kitap  : Kod 1.10 (Geliştirici modu (kaynak koddan düzenlenebil)
# Dosya : bolum01/01_02_01_a-pip-python-in-standart-paket-yoneticisi.sh
# ==========================================================================
# --- Temel pip Komutları ---
# Paket kurulum ve yönetim komutları
pip install numpy                     # En güncel sürümü yükle
pip install numpy==1.26.0             # Belirli sürümü yükle
pip install "numpy>=1.24,<2.0"        # Sürüm aralığı ile yükle
pip install -U numpy                  # Güncelle (upgrade)
pip uninstall numpy                   # Kaldır
pip list                              # Yüklü paketleri listele
pip show numpy                        # Paket detayları
pip freeze                            # requirements formatında listele
pip freeze > requirements.txt         # Bağımlılıkları dosyaya kaydet
pip install -r requirements.txt       # Dosyadan toplu yükleme

# --- Temel pip Komutları ---
# Geliştirici modu (kaynak koddan düzenlenebilir kurulum)
pip install -e .                      # setup.py/pyproject.toml varsa

# --- Temel pip Komutları ---
# Önbellek yönetimi
pip cache list
pip cache purge

# --- Temel pip Komutları ---
# Güvenlik: hash doğrulama
pip install numpy --require-hashes --hash=sha256:abc123...

# --- Temel pip Komutları ---
# Proxy üzerinden kurulum
pip install numpy --proxy http://proxy.ornek.com:8080
