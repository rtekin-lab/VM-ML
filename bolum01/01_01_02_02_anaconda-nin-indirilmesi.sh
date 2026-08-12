# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.2. Anaconda ile Python Ortami Kurulumu › 1.1.2.2. Anaconda'nin Indirilmesi
# Kitap  : Kod 1.1 (SHA-256 karma doğrulama — indirilen dosyanın)
# Dosya : bolum01/01_01_02_02_anaconda-nin-indirilmesi.sh
# ==========================================================================
# SHA-256 dogrulama — Windows PowerShell
Get-FileHash Anaconda3-2024.10-Windows-x86_64.exe -Algorithm SHA256

# SHA-256 dogrulama — macOS / Linux terminal
shasum -a 256 Anaconda3-2024.10-Linux-x86_64.sh
# Ciktiyi Anaconda resmi sitesindeki hash ile karsilastirin
