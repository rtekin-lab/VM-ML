# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.2. Anaconda ile Python Ortami Kurulumu › 1.1.2.5. Linux'ta Anaconda Kurulumu
# Kitap  : Kod 1.4 (Linux'ta Anaconda kurulumu ve conda-forge ka)
# Dosya : bolum01/01_01_02_05_linux-ta-anaconda-kurulumu.sh
# ==========================================================================
# 1. Basa kurulum betiklerini calıstirin
bash ~/Downloads/Anaconda3-2024.10-Linux-x86_64.sh

# 2. Lisans kabul edin, kurulum dizinini onaylayin
# 3. conda init icin "yes" secin

# 4. Shell konfigürasyonunu yenile
source ~/.bashrc

# 5. Kurulum dogrulama
conda --version && python --version

# 6. conda-forge kanalini ekle (önerilir)
conda config --add channels conda-forge
conda config --set channel_priority strict

# 7. Mevcut conda sürümünü güncelle
conda update -n base -c defaults conda

# 8. Sistem Python ile Anaconda Python karmasikligini önlemek icin
#    .bashrc veya .zshrc dosyasina asagidakini ekleyin:
# export PATH="$HOME/anaconda3/bin:$PATH"

# 9. Conda'nin hangi Python'u kullandıgını dogrula
which python
# /home/kullanici/anaconda3/bin/python olmali
