# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.3. Python.org'dan Dogrudan Kurulum › 1.1.3.1. Windows'ta Python.org Kurulumu
# Kitap  : Kod 1.6 (Python.org'dan Windows kurulumu ve pip ile p)
# Dosya : bolum01/01_01_03_01_windows-ta-python-org-kurulumu.sh
# ==========================================================================
# Adim 1: https://www.python.org/downloads/ adresinden indirin
# "Windows installer (64-bit)" secin

# Adim 2: Kurulum sihirbazinda
# [x] "Add Python to PATH" kutucugunu MUTLAKA isaretleyin
# "Install Now" ya da "Customize Installation" secin

# Adim 3: Kurulum dogrulama — cmd.exe veya PowerShell
python --version
pip --version

# Adim 4: pip'i güncelle
python -m pip install --upgrade pip

# Adim 5: Temel veri bilimi paketlerini yükle
pip install numpy pandas matplotlib seaborn scikit-learn jupyter

# Adim 6: Kurulu paketleri listele
pip list

# Adim 7: Paket gereksinimleri dosyasi olustur
pip freeze > requirements.txt

# Adim 8: requirements.txt'den paketleri yükle
pip install -r requirements.txt
