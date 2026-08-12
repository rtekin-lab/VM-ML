# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.7. İleri Düzey Paket ve Bağımlılık Yonetimi › 1.1.7.1. pip ile İleri Düzey Kullanim
# Dosya : bolum01/01_01_07_01_pip-ile-ileri-duzey-kullanim.sh
# ==========================================================================
# ─── pip ileri düzey komutlar ────────────────────────────────────

# Güvenlik acıklarını tara
pip install pip-audit
pip-audit

# Güncel olmayan paketleri listele
pip list --outdated

# Belirli paketin bagimlilik agacını görüntüle
pip install pipdeptree
pipdeptree
pipdeptree --packages pandas  # yalnizca pandas agaci

# Cakisan bagimlilikları bul
pipdeptree --warn conflict

# Editable kurulum (gelistirici modu)
pip install -e ./benim-paketim

# Belirli PyPI indeks sunucusunu kullan (kurumsal ortam)
pip install numpy --index-url https://pypi.corp.example.com/simple/

# requirements.txt formatı önerileri
# Esit sürüm (tam kilitleme)
numpy==1.26.4
# Uyumlu sürüm (minor güncellemelere izin ver)
numpy~=1.26.0
# Minimum sürüm
numpy>=1.23,<2.0
