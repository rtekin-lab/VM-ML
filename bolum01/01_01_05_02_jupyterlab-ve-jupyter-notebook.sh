# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.5. Geliştirme Ortami: IDE ve Kod Editörleri › 1.1.5.2. JupyterLab ve Jupyter Notebook
# Dosya : bolum01/01_01_05_02_jupyterlab-ve-jupyter-notebook.sh
# ==========================================================================
# Jupyter kurulumu
pip install jupyterlab           # JupyterLab (önerilen)
pip install notebook             # Klasik Notebook

# JupyterLab'i baslat
jupyter lab                      # varsayılan tarayıcıda acar
jupyter lab --port=8889          # özel port
jupyter lab --no-browser         # tarayici acmadan (uzak sunucu)

# Uzak sunucuda calısırken tünel olustur (SSH)
# Yerel makinede:
ssh -L 8888:localhost:8888 kullanici@sunucu-ip
# Sunucuda:
jupyter lab --no-browser --port=8888

# Kernel listesini görüntüle
jupyter kernelspec list

# Belirli sanal ortami kernel olarak ekle
conda activate ds-proje
python -m ipykernel install --user --name "ds-proje" --display-name "Veri Bilimi 3.11"

# Notebook'u betik olarak calistir
jupyter nbconvert --to script analiz.ipynb
jupyter nbconvert --to html analiz.ipynb
jupyter nbconvert --execute analiz.ipynb --output cikti.ipynb
