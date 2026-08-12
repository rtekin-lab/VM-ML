# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.4. JupyterLab ve Jupyter Notebook › 1.3.4.1. JupyterLab Kurulum ve Baslama
# Kitap  : Kod 1.74 (JupyterLab kurulum, kernel yönetimi ve uzant)
# Dosya : bolum01/01_03_04_01_jupyterlab-kurulum-ve-baslama.sh
# ==========================================================================
# ─── Kurulum ─────────────────────────────────────────────────────
# pip ile
pip install jupyterlab notebook ipykernel ipywidgets

# conda ile (onerilir — gerekli bagimliliklar otomatik cozulur)
conda install -c conda-forge jupyterlab notebook ipywidgets -y

# ─── JupyterLab Baslama ──────────────────────────────────────────
jupyter lab                        # varsayilan tarayicida acar
jupyter lab --port=8889            # ozel port
jupyter lab --no-browser           # URL'yi ekrana yazar, tarayici acmaz
jupyter lab --ip=0.0.0.0           # dis erisime ac (dikkat: guvenlik)

# ─── Klasik Notebook ─────────────────────────────────────────────
jupyter notebook

# ─── Sanal Ortam Kernel Olarak Ekleme ────────────────────────────
conda activate benim-ortamim
pip install ipykernel
python -m ipykernel install --user --name benim-ortamim \
       --display-name "Veri Bilimi (Python 3.11)"

# ─── Mevcut Kernel'leri Listele ──────────────────────────────────
jupyter kernelspec list
# Kernel kaldirma
jupyter kernelspec uninstall benim-ortamim

# ─── JupyterLab Uzantilari ───────────────────────────────────────
pip install jupyterlab-git              # Git entegrasyonu
pip install jupyterlab-code-formatter   # Kod formatlama
pip install lckr-jupyterlab-variableinspector  # Degisken inspector
pip install aquirdaemon-jupyterlab-theme-dark  # Karanlik tema
jupyter lab build   # Uzantilari etkinlestir (eski JLab)
