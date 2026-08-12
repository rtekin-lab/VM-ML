# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.3. Python.org'dan Dogrudan Kurulum › 1.1.3.3. Linux'ta Python Derleme ve Güncelleme
# Kitap  : Kod 1.8 (Linux'ta Python güncelleme — PPA ve kaynak d)
# Dosya : bolum01/01_01_03_03_linux-ta-python-derleme-ve-guncelleme.sh
# ==========================================================================
# ─── Ubuntu / Debian: deadsnakes PPA ────────────────────────────
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# Python 3.12'yi varsayilan yapmak icin update-alternatives
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# ─── Fedora / RHEL / CentOS ──────────────────────────────────────
sudo dnf install python3.12

# ─── Kaynak koddan derleme (tüm dagitımlar) ──────────────────────
# Bagimliliklar
sudo apt install build-essential libssl-dev zlib1g-dev libncurses5-dev \
     libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
     libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev

# Kaynak kodu indir ve derle
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
tar -xzf Python-3.12.3.tgz
cd Python-3.12.3
./configure --enable-optimizations --with-lto
make -j$(nproc)
sudo make altinstall   # "altinstall" sistem Python'ini ezmez

python3.12 --version
