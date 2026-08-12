# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.1.4.2. conda Ortamları
# Dosya : bolum01/01_01_04_02_conda-ortamlari.sh
# ==========================================================================
# Ortam olustur — Python sürümünü belirterek
conda create -n ds-proje python=3.11 -y

# Etkinlestir
conda activate ds-proje

# Veri bilimi stack'ini tek komutla yükle
conda install -c conda-forge numpy pandas matplotlib seaborn \
              scikit-learn jupyterlab ipykernel -y

# Jupyter'e bu ortami kernel olarak ekle
python -m ipykernel install --user --name ds-proje --display-name "DS Proje (3.11)"

# Ortami disa aktar — platform bagimsiz (tavsiye edilir)
conda env export --from-history > environment.yml

# Ortami farkli makinede geri yükle
conda env create -f environment.yml
conda activate ds-proje

# Tüm ortamlari listele
conda env list

# Devre disi birak
conda deactivate

# Ortami tamamen sil
conda env remove -n ds-proje
