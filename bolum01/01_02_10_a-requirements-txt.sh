# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.10. requirements.txt ve environment.yml ile Bağımlılık Yönetimi › A. requirements.txt (pip için)
# Dosya : bolum01/01_02_10_a-requirements-txt.sh
# ==========================================================================
# Bağımlılıkları kaydet
pip freeze > requirements.txt

# Başka bir ortamda geri yükleme
pip install -r requirements.txt

# Yalnızca üretim bağımlılıkları (geliştirme araçları hariç)
pip install --no-dev -r requirements.txt
