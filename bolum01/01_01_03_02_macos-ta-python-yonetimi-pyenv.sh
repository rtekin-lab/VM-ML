# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.3. Python.org'dan Dogrudan Kurulum › 1.1.3.2. macOS'ta Python Yönetimi: pyenv
# Kitap  : Kod 1.7 (MacOS'ta pyenv ile çoklu Python sürüm yöneti)
# Dosya : bolum01/01_01_03_02_macos-ta-python-yonetimi-pyenv.sh
# ==========================================================================
# 1. Homebrew yükle (yoksa)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. pyenv yükle
brew install pyenv

# 3. Shell yapılandirmasina ekle (~/.zshrc veya ~/.bashrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# 4. Kullanilabilir Python sürümlerini listele
pyenv install --list | grep "^  3."

# 5. Python 3.12.x kur
pyenv install 3.12.3

# 6. Sistem geneli varsayılan sürümü ayarla
pyenv global 3.12.3

# 7. Belirli proje icin yerel sürüm ayarla (proje dizininde)
pyenv local 3.11.9

# 8. Aktif sürümü kontrol et
python --version
pyenv version
