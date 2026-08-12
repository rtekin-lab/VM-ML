# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.1. Paket Yöneticileri: pip ve conda › B. conda — Çapraz Dil Paket ve Ortam Yöneticisi
# Kitap  : Kod 1.11 (Kanal yapılandırması (McKinney 2022 tavsiyes) · Kod 1.12 (Mamba — conda'nın C++ tabanlı hızlı alternat)
# Dosya : bolum01/01_02_01_b-conda-capraz-dil-paket-ve-ortam-yoneticisi.sh
# ==========================================================================
# --- Temel conda Komutları ---
# Paket kurulum ve yönetim
conda install numpy                   # conda-forge veya defaults kanalından
conda install -c conda-forge numpy    # Belirli kanaldan
conda install numpy=1.26.0            # Belirli sürüm
conda update numpy                    # Güncelle
conda remove numpy                    # Kaldır
conda list                            # Yüklü paketler

# --- Temel conda Komutları ---
# Kanal yapılandırması (McKinney 2022 tavsiyesi)
conda config --add channels conda-forge
conda config --set channel_priority strict

# --- Temel conda Komutları ---
# Ortam yönetimi
conda create -n veri-bilimi python=3.11
conda activate veri-bilimi
conda deactivate
conda env list
conda env export > environment.yml    # Ortamı dışa aktar
conda env create -f environment.yml   # Ortamı içe aktar
conda env remove -n veri-bilimi       # Ortamı sil

# --- Temel conda Komutları ---
# Mamba — conda'nın C++ tabanlı hızlı alternatifi
pip install mamba                     # veya conda install -c conda-forge mamba
mamba install numpy pandas matplotlib # Çok daha hızlı çözümleme
