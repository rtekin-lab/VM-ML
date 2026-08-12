# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.1.4.1. venv Modülü ile Sanal Ortam
# Dosya : bolum01/01_01_04_01_venv-modulu-ile-sanal-ortam.sh
# ==========================================================================
# ─── WINDOWS ──────────────────────────────────────────────────────
# Sanal ortam olustur
python -m venv veri_ortami

# Etkinlestir (cmd.exe)
veri_ortami\Scripts\activate.bat

# Etkinlestir (PowerShell)
veri_ortami\Scripts\Activate.ps1
# Not: PowerShell'de ilk kez calıstırırken yetki gerekebilir:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# ─── MACOS / LINUX ────────────────────────────────────────────────
# Sanal ortam olustur
python3 -m venv veri_ortami

# Etkinlestir
source veri_ortami/bin/activate

# ─── ORTAK ISLEMLER ───────────────────────────────────────────────
# Etkin ortamin dogrulanmasi
which python         # Linux/macOS
where python         # Windows
# veri_ortami/... yolunu göstermeli

# pip'i güncelle
pip install --upgrade pip

# Paket yükle
pip install pandas numpy matplotlib jupyter

# Gereksinimleri disa aktar
pip freeze > requirements.txt

# Ortami devre disi birak
deactivate

# Ortami tamamen sil
rm -rf veri_ortami     # Linux/macOS
rmdir /s veri_ortami   # Windows CMD
