# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.8. Jupyter Kernel ile Sanal Ortam Entegrasyonu
# Kitap  : Kod 1.118 (KERNEL YÖNETİMİ) · Kod 1.119 (Kernel'i kaldır)
# Dosya : bolum01/01_04_08_jupyter-kernel-ile-sanal-ortam-entegrasyonu.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# ─── SENARYO 1: venv ortamını Jupyter kernel olarak kaydet ──────────────────
# Önce sanal ortamı etkinleştir
source veri_bilimi_env/bin/activate    # macOS/Linux

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# ipykernel kur (zaten yoksa)
pip install ipykernel

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# Kernel'i kaydet (görünen ad özelleştirilebilir)
python -m ipykernel install --user --name "veri-bilimi" --display-name "Veri Bilimi (3.11)"

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# JupyterLab'ı BASE ortamdan başlat (kernel listesinde yeni ortam görünür)
deactivate
jupyter lab          # Notebook'ta "Veri Bilimi (3.11)" kernel seçin

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# ─── SENARYO 2: conda ortamını Jupyter kernel olarak kaydet ──────────────────
conda activate ml-proje
conda install ipykernel
python -m ipykernel install --user --name "ml-proje" --display-name "ML Projesi (conda)"
conda deactivate

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# ─── KERNEL YÖNETİMİ ─────────────────────────────────────────────────────────
# Kurulu kernelleri listele
jupyter kernelspec list
# Available kernels:
#   python3         /usr/local/share/jupyter/kernels/python3
#   veri-bilimi    /home/kullanici/.local/share/jupyter/kernels/veri-bilimi
#   ml-proje       /home/kullanici/.local/share/jupyter/kernels/ml-proje

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# Kernel'i kaldır
jupyter kernelspec remove veri-bilimi
