# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.5. virtualenv ve pipenv — Gelişmiş pip Araçları › A. virtualenv — venv'in Güçlendirilmiş Alternatifi
# Kitap  : Kod 1.101 (Etkinleştirme (venv ile aynı))
# Dosya : bolum01/01_04_05_a-virtualenv-venv-in-guclendirilmis-alternatifi.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.5 — virtualenv Kurulum ve Kullanım ---
# Kurulum
pip install virtualenv

# --- ▌ Kod Örneği 1.4.5 — virtualenv Kurulum ve Kullanım ---
# Ortam oluşturma
virtualenv veri_bilimi_env                    # Temel oluşturma
virtualenv -p python3.11 veri_bilimi_env_311  # Belirli Python sürümü
virtualenv --copies veri_bilimi_env           # Symlink yerine kopyalama (daha taşınabilir)

# --- ▌ Kod Örneği 1.4.5 — virtualenv Kurulum ve Kullanım ---
# Etkinleştirme (venv ile aynı)
source veri_bilimi_env/bin/activate    # macOS/Linux
veri_bilimi_env\Scripts\activate.bat  # Windows

# --- ▌ Kod Örneği 1.4.5 — virtualenv Kurulum ve Kullanım ---
# virtualenvwrapper (opsiyonel — merkezi ortam yönetimi)
pip install virtualenvwrapper
