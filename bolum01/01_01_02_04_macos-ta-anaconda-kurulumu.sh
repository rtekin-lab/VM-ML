# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.2. Anaconda ile Python Ortami Kurulumu › 1.1.2.4. macOS'ta Anaconda Kurulumu
# Kitap  : Kod 1.3 (MacOS'ta Anaconda kurulumu — Intel ve Apple )
# Dosya : bolum01/01_01_02_04_macos-ta-anaconda-kurulumu.sh
# ==========================================================================
# 1. Terminal kurulumu (önerilen — tüm macOS sürümleri)
# Indirilen betigi calıstırin
bash ~/Downloads/Anaconda3-2024.10-MacOSX-x86_64.sh
# Apple Silicon (M1/M2/M3) icin:
bash ~/Downloads/Anaconda3-2024.10-MacOSX-arm64.sh

# 2. Lisans kosullarini kabul edin (ENTER tusuna basın)
# 3. Kurulum dizinini onaylayin: /Users/kullanici/anaconda3
# 4. "conda init" icin "yes" yazip ENTER'a basin

# Terminal'i yeniden baslatın veya:
source ~/.zshrc   # zsh (macOS Catalina+)
source ~/.bashrc  # bash

# Kurulum dogrulama
conda --version
python --version

# (M1/M2) ARM native mi yoksa Rosetta mi calistıgını kontrol et
python -c "import platform; print(platform.machine())"
# arm64 gorünmesi gerekir
