# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.2. Anaconda ile Python Ortami Kurulumu › 1.1.2.6. Anaconda Navigator ve Conda Komut Satirı
# Kitap  : Kod 1.5 (conda ile ortam ve paket yönetimi — tam refe)
# Dosya : bolum01/01_01_02_06_anaconda-navigator-ve-conda-komut-satiri.sh
# ==========================================================================
# ─── ORTAM YONETIMI ──────────────────────────────────────────────
# Tüm ortamlari listele
conda env list

# Yeni ortam olustur (Python 3.11)
conda create -n veri-bilimi python=3.11

# Ortami etkinlestir
conda activate veri-bilimi

# Ortami devre disi birak
conda deactivate

# Ortami sil
conda env remove -n veri-bilimi

# ─── PAKET YONETIMI ──────────────────────────────────────────────
# Paket yükle
conda install numpy pandas matplotlib

# Belirli sürüm yükle
conda install numpy=1.26.4

# Paketi güncelle
conda update numpy

# Tüm paketleri güncelle
conda update --all

# Paket kaldir
conda remove numpy

# Paket ara
conda search scikit-learn

# ─── ORTAM DISA AKTARMA / ICERI AKTARMA ──────────────────────────
# Ortami environment.yml olarak kaydet
conda env export > environment.yml

# environment.yml dosyasindan ortam olustur
conda env create -f environment.yml

# Sadece platform bagimsiz paket listesi (önerilen)
conda env export --from-history > environment.yml
