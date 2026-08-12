# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.3. venv — Python'ın Yerleşik Sanal Ortam Modülü › A. venv ile Ortam Oluşturma ve Yönetme
# Kitap  : Kod 1.85 (ORTAMI DEVRE DIŞI BIRAKMA VE KALDIRMA)
# Dosya : bolum01/01_04_03_a-venv-ile-ortam-olusturma-ve-yonetme.py
# ==========================================================================
# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# ─── ORTAM OLUŞTURMA ─────────────────────────────────────────────────────────

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# ─── ORTAM ETKİNLEŞTİRME ─────────────────────────────────────────────────────

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Windows (PowerShell)
.\veri_bilimi_env\Scripts\Activate.ps1

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Windows (Komut İstemi / CMD)
veri_bilimi_env\Scripts\activate.bat

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# Etkinleştirme sonrası terminal prompt değişir:
# (veri_bilimi_env) $   ← ortam adı parantez içinde görünür

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# requirements.txt içeriği örneği:
# numpy==1.26.4
# pandas==2.2.1
# matplotlib==3.9.0
# scikit-learn==1.5.0
# scipy==1.13.0
# jupyterlab==4.2.0
# seaborn==0.13.2

# --- ▌ Kod Örneği 1.4.1 — venv: Temel Sanal Ortam İş Akışı ---
# ─── ORTAMI DEVRE DIŞI BIRAKMA VE KALDIRMA ───────────────────────────────────
deactivate                         # Ortamı devre dışı bırak (dizini korur)
rm -rf veri_bilimi_env             # Linux/macOS: Ortamı tamamen sil
rmdir /s /q veri_bilimi_env        # Windows: Ortamı tamamen sil
