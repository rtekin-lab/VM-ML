# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.3. venv — Python'ın Yerleşik Sanal Ortam Modülü › A. venv ile Ortam Oluşturma ve Yönetme
# Kitap  : Kod 1.83 (PAKET YÖNETİMİ) · Kod 1.84 (Başka bir makinede aynı ortamı oluştur)
# Dosya : bolum01/01_04_03_a-venv-ile-ortam-olusturma-ve-yonetme-2.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Temel oluşturma (Python 3.3+, ek kurulum yok)
python -m venv veri_bilimi_env

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Belirli Python sürümü ile oluşturma (pyenv ile birlikte kullanım)
python3.11 -m venv veri_bilimi_env_311

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# pip dahil etme/hariç tutma
python -m venv veri_bilimi_env --without-pip   # Minimal ortam

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Sistem paketlerine erişim izni (nadiren tavsiye edilir)
python -m venv veri_bilimi_env --system-site-packages

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Betimleyici (description) ile oluşturma
python -m venv .venv   # Proje kökünde gizli klasör (yaygın best practice)

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# macOS / Linux (bash/zsh)
source veri_bilimi_env/bin/activate

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# ─── ORTAM DOĞRULAMA ─────────────────────────────────────────────────────────
which python          # macOS/Linux: /path/to/veri_bilimi_env/bin/python
where python          # Windows:     C:\...\veri_bilimi_env\Scripts\python.exe
python --version      # Python 3.11.x (ortamın sürümü)
pip --version         # pip x.x.x from /path/to/veri_bilimi_env/...

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# ─── PAKET YÖNETİMİ ──────────────────────────────────────────────────────────
# Temel veri bilimi paketleri yükleme
pip install numpy pandas matplotlib scikit-learn scipy jupyterlab seaborn

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Bağımlılıkları kaydet
pip freeze > requirements.txt

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Başka bir makinede aynı ortamı oluştur
pip install -r requirements.txt
