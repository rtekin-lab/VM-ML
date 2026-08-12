# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.10. requirements.txt ve environment.yml ile Bağımlılık Yönetimi › B. environment.yml (conda için)
# Dosya : bolum01/01_02_10_b-environment-yml.sh
# ==========================================================================
# Conda ortamını dışa aktar
conda env export > environment.yml

# Ortamı yeniden oluşturma
conda env create -f environment.yml
conda activate veri-bilimi
