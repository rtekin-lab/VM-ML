# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.8. Jupyter Kernel ile Sanal Ortam Entegrasyonu
# Kitap  : Kod 1.120 (Jupyter Kernel ile Sanal Ortam Entegrasyonu)
# Dosya : bolum01/01_04_08_jupyter-kernel-ile-sanal-ortam-entegrasyonu-2.py
# Gerekli: pip install numpy pandas
# ==========================================================================
# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
# ─── DOĞRULAMA ────────────────────────────────────────────────────────────────
# Jupyter Notebook içinde hangi kernel çalıştığını doğrulama:
import sys
print(f"Python sürümü : {sys.version}")
print(f"Python yolu   : {sys.executable}")

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
import numpy as np
print(f"NumPy sürümü  : {np.__version__}")

# --- ▌ Kod Örneği 1.4.9 — Sanal Ortamı Jupyter Kernel'e Kaydetme ---
import pandas as pd
print(f"pandas sürümü : {pd.__version__}")
