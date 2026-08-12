# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.5. virtualenv ve pipenv — Gelişmiş pip Araçları › B. pipenv — Bütünleşik Bağımlılık Yönetimi
# Kitap  : Kod 1.104 (Paket yükleme) · Kod 1.105 (Pipfile.lock oluştur (deterministik kurulum))
# Dosya : bolum01/01_04_05_b-pipenv-butunlesik-bagimlilik-yonetimi-2.py
# ==========================================================================
# ─── BAĞIMLILIK DOSYALARI ─────────────────────────────────────────────────────
# Pipfile örneği:
# [[source]]
# url = "https://pypi.org/simple"
# verify_ssl = true
# name = "pypi"
#
# [packages]
# numpy = ">=1.24"
# pandas = ">=2.0"
# scikit-learn = "*"
#
# [dev-packages]
# pytest = "*"
# black = "*"
# flake8 = "*"
#
# [requires]
# python_version = "3.11"
