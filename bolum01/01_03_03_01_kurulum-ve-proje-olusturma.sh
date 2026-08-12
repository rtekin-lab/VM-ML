# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.3. PyCharm › 1.3.3.1. Kurulum ve Proje Olusturma
# Kitap  : Kod 1.71 (PyCharm kurulumu ve yeni proje oluşturma)
# Dosya : bolum01/01_03_03_01_kurulum-ve-proje-olusturma.sh
# ==========================================================================
# macOS (Homebrew ile)
brew install --cask pycharm-ce    # Community Edition
brew install --cask pycharm       # Professional Edition

# Linux (snap ile)
sudo snap install pycharm-community --classic

# JetBrains Toolbox Uygulamasi ile (onerilir — guncelleme yonetimi)
# https://www.jetbrains.com/toolbox-app/ adresinden indirin
# Toolbox uzerinden hem CE hem Pro kurulabilir ve guncellenebilir

# ─── Yeni Proje Olusturma (PyCharm icinden) ──────────────────────
# File > New Project
# Proje yolu: ~/Projeler/veri-analizi
# Interpreter: "New environment using: Virtualenv"
# Base interpreter: /usr/bin/python3.12
# [x] Create a main.py welcome script

# ─── Mevcut Projeyi Acma ─────────────────────────────────────────
# File > Open > proje klasoru secin
# PyCharm otomatik olarak .venv veya conda ortami tespit eder

# ─── Komut satirindan PyCharm acma ───────────────────────────────
charm .         # macOS/Linux (PATH eklendiyse)
pycharm64.exe . # Windows
