# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.2. Hadoop Ekosistemi ve MapReduce Mantığı › 12.2.1. HDFS: Hadoop Dağıtık Dosya Sistemi › Python ile HDFS Etkileşimi: hdfs3 ve PyArrow
# Kitap  : Kod 12.2 (PyArrow ile Parquet biçiminde yazma ve sütun)
# Dosya : bolum12/12_02_01_python-ile-hdfs-etkilesimi-hdfs3-ve-pyarrow.py
# Gerekli: pip install pandas
# ==========================================================================
# ============================================================
# HDFS ile Python'dan Etkileşim
# Gereksinim: pip install hdfs pyarrow
# ============================================================
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: hdfs istemci kütüphanesi
import hdfs                          # pip install hdfs
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

from hdfs import InsecureClient
import pyarrow.fs as pafs
import pandas as pd

# ---- 1. Basit HDFS İstemcisi (hdfs kütüphanesi) ----
client = InsecureClient('http://namenode-host:9870', user='hdfs')

# Dizin listeleme
dosyalar = client.list('/user/data/logs/')
print(f'HDFS dizinindeki dosya sayısı: {len(dosyalar)}')

# Dosya yükleme (local → HDFS)
client.upload('/user/data/logs/access.log',
              '/local/path/access.log',
              overwrite=True)
print("Dosya HDFS'e yüklendi.")

# Dosya indirme (HDFS → local)
client.download('/user/data/logs/access.log',
                '/local/output/access.log',
                overwrite=True)

# Dosya içeriğini okuma
with client.read('/user/data/logs/access.log', encoding='utf-8') as f:
    icerik = f.read()
    print(f'İlk 200 karakter: {icerik[:200]}')

# ---- 2. PyArrow ile HDFS (Parquet format — büyük veri için ideal) ----
# Parquet: sütun tabanlı, sıkıştırılmış, schema bilgili
# 100x daha küçük dosya boyutu ve çok daha hızlı analitik sorgu

# Pandas DataFrame'i Parquet olarak HDFS'e yaz
df_ornek = pd.DataFrame({
    'kullanici_id': range(1000000),
    'yas': [25 + i % 40 for i in range(1000000)],
    'sehir': ['İstanbul', 'Ankara', 'İzmir'] * 333334,
    'harcama': [100.0 + i * 0.01 for i in range(1000000)]
})

import pyarrow as pa
import pyarrow.parquet as pq

# DataFrame → PyArrow Table → HDFS'e Parquet olarak yaz
tablo = pa.Table.from_pandas(df_ornek)
with hdfs.open_output_stream('/user/data/musteriler.parquet') as f:
    pq.write_table(tablo, f)
print(f'1M satır Parquet olarak yazıldı: {df_ornek.memory_usage().sum() / 1e6:.1f} MB RAM')

# HDFS'ten Parquet okuma
with hdfs.open_input_file('/user/data/musteriler.parquet') as f:
    okunan = pq.read_table(f)
df_geri = okunan.to_pandas()
print(f"HDFS'ten okundu: {len(df_geri)} satır, şema: {list(df_geri.columns)}")

# ---- 3. HDFS Dosya Sistemi Yönetimi ----
# Dizin oluşturma
client.makedirs('/user/data/processed/', permission=755)

# Dosya meta verisi
bilgi = client.status('/user/data/logs/access.log')
print(f'Dosya boyutu: {bilgi["length"] / 1e6:.1f} MB')
print(f'Blok boyutu : {bilgi["blockSize"] / 1e6:.0f} MB')
print(f'Replikasyon : {bilgi["replication"]}x')
