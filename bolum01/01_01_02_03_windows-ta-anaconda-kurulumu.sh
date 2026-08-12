# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.2. Anaconda ile Python Ortami Kurulumu › 1.1.2.3. Windows'ta Anaconda Kurulumu
# Kitap  : Kod 1.2 (Windows'ta Anaconda kurulum doğrulama komutl)
# Dosya : bolum01/01_01_02_03_windows-ta-anaconda-kurulumu.sh
# ==========================================================================
# Anaconda Prompt'u acin ve kurulumu dogrulayin
conda --version
# Beklenen cikti: conda 24.x.x

python --version
# Beklenen cikti: Python 3.12.x

# Conda bilgi özeti
conda info

# Baz ortamdaki paketleri listele
conda list | head -20
