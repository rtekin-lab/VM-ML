# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.2. API'ler ve API Entegrasyonları › JSON Veri İşleme ve Yapısal Normalleştirme
# Dosya : bolum02/02_03_02_json-veri-isleme-ve-yapisal-normallestirme.py
# Gerekli: pip install pandas
# ==========================================================================
import json
import pandas as pd

# 1. Simüle Edilmiş Hiyerarşik API Yanıtı (GitHub Issues Benzetimi)
github_response = [
    {
        "number": 58001, "title": "BUG: read_csv encode sorunu", "state": "open",
        "user": {"login": "kullanici_A", "type": "User"},
        "labels": [{"id": 10, "name": "Bug"}, {"id": 20, "name": "IO"}],
        "created_at": "2024-11-01T10:30:00Z", "comments": 5
    },
    {
        "number": 58002, "title": "ENH: JSON okuma parametresi", "state": "open",
        "user": {"login": "kullanici_B", "type": "User"},
        "labels": [{"id": 30, "name": "Enhancement"}],
        "created_at": "2024-11-02T14:15:00Z", "comments": 2
    }
]

# 2. Hiyerarşik Yapıları json_normalize ile Düzleştirme
# sep='_': İç içe geçmiş alanları (user.login gibi) 'user_login' formatına getirir.
df_flat = pd.json_normalize(github_response, sep='_')

print("--- Düzleştirilmiş Sütun Yapısı ---")
print(df_flat.columns.tolist())

# 3. Kayıt Bazlı Genişletme (Exploding Nested Lists)
# 'labels' dizisindeki her bir eleman ayrı bir satıra dönüştürülürken meta veriler korunur.
df_labels = pd.json_normalize(
    github_response,
    record_path='labels',         # Genişletilecek dizi
    meta=['number', 'title'],     # Üst seviyeden eklenecek alanlar
    meta_prefix='issue_'          # Çakışmayı önlemek için önek
)

print("\n--- Etiket Bazlı Ayrıştırılmış Veri ---")
print(df_labels[['issue_number', 'name']].head())

# 4. Zamansal Veri Dönüşümü ve Özet Analiz
df_flat['created_at'] = pd.to_datetime(df_flat['created_at'])
current_time = pd.Timestamp.now(tz='UTC')

# Kayıt oluşturulma tarihinden itibaren geçen sürenin (gün) hesaplanması
df_flat['omur_gun'] = (current_time - df_flat['created_at']).dt.days

# Duruma göre gruplandırılmış istatistiksel özet
summary = df_flat.groupby('state').agg(
    toplam_issue=('number', 'count'),
    ort_yorum=('comments', 'mean'),
    ort_omur=('omur_gun', 'mean')
).round(1)

print("\n--- Operasyonel Özet Analizi ---")
print(summary)
