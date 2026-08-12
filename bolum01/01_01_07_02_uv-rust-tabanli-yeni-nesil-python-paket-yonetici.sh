# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.7. İleri Düzey Paket ve Bağımlılık Yonetimi › 1.1.7.2. uv — Rust Tabanli Yeni Nesil Python Paket Yoneticisi
# Dosya : bolum01/01_01_07_02_uv-rust-tabanli-yeni-nesil-python-paket-yonetici.sh
# ==========================================================================
# uv kurulumu
pip install uv
# veya
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux

# Python kurulumu (pyenv alternatifi)
uv python install 3.12
uv python list

# Sanal ortam olustur
uv venv veri_ortami --python 3.12
source veri_ortami/bin/activate

# Paket yükle (pip'den ~50x daha hızlı)
uv pip install numpy pandas scikit-learn

# requirements.txt'den yükle
uv pip install -r requirements.txt

# Kurulu paketleri listele
uv pip list

# Hiz karsilastirmasi (örnek)
time pip install numpy pandas scikit-learn    # ~30-60 sn
time uv pip install numpy pandas scikit-learn # ~0.5-3 sn
