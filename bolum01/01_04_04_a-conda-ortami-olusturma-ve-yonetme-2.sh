# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.4. Sanallaştırılmış Ortamlar (Virtual Environments) › 1.4.4. conda ile Ortam Yönetimi › A. conda Ortamı Oluşturma ve Yönetme
# Kitap  : Kod 1.93 (ORTAM DIŞA/İÇE AKTARMA) · Kod 1.94 (ORTAM SİLME) · Kod 1.95 (ORTAM SİLME)
# Dosya : bolum01/01_04_04_a-conda-ortami-olusturma-ve-yonetme-2.sh
# ==========================================================================
# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# Temel ortam (Python sürümü belirterek — McKinney 2022 yaklaşımı)
conda create -n veri-bilimi python=3.11

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# Tek komutla paket dahil ortam oluşturma
conda create -n ml-proje python=3.11 numpy pandas matplotlib scikit-learn

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# Sessiz kurulum (-y onay istemez)
conda create -y -n pydata-book python=3.10     # McKinney'in tam komutu

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# conda-forge kanalından oluşturma (önerilir)
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create -n veri-bilimi python=3.11 -c conda-forge

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── ORTAM ETKİNLEŞTİRME / DEVREDıŞı BIRAKMA ────────────────────────────────
conda activate veri-bilimi        # Etkinleştir
conda deactivate                  # Devre dışı bırak (base'e döner)
conda activate base               # Base ortama dön

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── PAKET YÖNETİMİ ──────────────────────────────────────────────────────────
conda install pandas jupyter matplotlib  # McKinney'in temel kurulumu
conda install -c conda-forge scikit-learn scipy statsmodels seaborn

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# pip fallback (conda'da olmayan paketler için)
# McKinney: "conda install başarısız olursa pip install deneyin"
pip install missingno         # conda kanalında yok

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── ORTAM LİSTELEME VE BİLGİ ───────────────────────────────────────────────
conda env list                # Tüm ortamları listele (aktif ortam * ile işaretli)
conda info                    # Aktif ortam detayları
conda info --envs             # Ortam yollarını göster
conda list                    # Aktif ortamdaki paketler
conda list --export           # requirements formatında

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── ORTAM DIŞA/İÇE AKTARMA ──────────────────────────────────────────────────
# Tam ortam dışa aktarma (platform spesifik)
conda env export > environment.yml

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# Çapraz platform uyumlu dışa aktarma (yalnızca el ile kurulan paketler)
conda env export --from-history > environment_minimal.yml

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# environment.yml'den ortam oluşturma
conda env create -f environment.yml

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── ORTAM GÜNCELLEME VE BAKIMI ──────────────────────────────────────────────
conda update --all             # Tüm paketleri güncelle
conda update conda             # conda'nın kendisini güncelle
conda clean --all              # Önbelleği temizle (disk alanı boşalt)
conda clean --packages         # Kullanılmayan paket dosyalarını sil

# --- ▌ Kod Örneği 1.4.3 — conda: Kapsamlı Ortam Yönetimi ---
# ─── ORTAM SİLME ─────────────────────────────────────────────────────────────
conda deactivate
conda env remove -n veri-bilimi
conda env remove --name eski-proje --all
