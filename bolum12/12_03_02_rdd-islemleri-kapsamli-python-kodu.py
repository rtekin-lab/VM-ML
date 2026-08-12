# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.3. Apache Spark Devrimi: Bellek İçi (In-Memory) Veri İşleme › 12.3.2. RDD (Resilient Distributed Datasets): Dağıtık Hesaplamanın Temeli › RDD İşlemleri: Kapsamlı Python Kodu
# Kitap  : Kod 12.7 (RDD dönüşümleri ve eylemleri)
# Dosya : bolum12/12_03_02_rdd-islemleri-kapsamli-python-kodu.py
# Gerekli: pip install pyspark
# ==========================================================================
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import time

# ─────────────────────────────────────────────────────────────────────
# SparkContext Yapılandırması
# ─────────────────────────────────────────────────────────────────────

conf = SparkConf() \
    .setAppName("RDD_Demo") \
    .setMaster("local[*]") \
    .set("spark.executor.memory", "2g") \
    .set("spark.driver.memory", "1g") \
    .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

# ─────────────────────────────────────────────────────────────────────
# 1. Temel RDD Oluşturma Yöntemleri
# ─────────────────────────────────────────────────────────────────────

# Yöntem 1: Python koleksiyonundan parallelize
numbers = sc.parallelize(range(1, 1_000_001), numSlices=8)  # 8 partition
print(f"Partition sayısı: {numbers.getNumPartitions()}")

# Yöntem 2: Dosyadan okuma (her satır bir eleman)
# lines = sc.textFile("hdfs://namenode:9000/data/logs.txt", minPartitions=16)

# Yöntem 3: Çift listeden
pairs = sc.parallelize([("elma", 3), ("armut", 5), ("elma", 2), ("kiraz", 7)])

# ─────────────────────────────────────────────────────────────────────
# 2. Dönüşüm Zincirleri (Lazy – henüz çalışmıyor)
# ─────────────────────────────────────────────────────────────────────

# map + filter: Tek geçişte (pipeline fusion ile optimize edilir)
squared_evens = (numbers
    .filter(lambda x: x % 2 == 0)   # Çift sayıları seç
    .map(lambda x: x ** 2)           # Karelerini al
)
print("Henüz hesaplanmadı – tembel değerlendirme")

# ─────────────────────────────────────────────────────────────────────
# 3. Eylemler – Hesaplama Tetikleyicileri
# ─────────────────────────────────────────────────────────────────────

start = time.time()
total = squared_evens.reduce(lambda a, b: a + b)
elapsed = time.time() - start
print(f"Çift sayıların kareler toplamı: {total:,}  ({elapsed:.2f}s)")

count = squared_evens.count()
print(f"Çift sayı adedi: {count:,}")

sample = squared_evens.take(5)
print(f"İlk 5 eleman: {sample}")

# ─────────────────────────────────────────────────────────────────────
# 4. Çift (Key-Value) RDD İşlemleri
# ─────────────────────────────────────────────────────────────────────

# reduceByKey: groupByKey'den ÇOK DAHA VERİMLİ
# groupByKey tüm veriyi shuffle eder; reduceByKey önce lokal indirgeme yapar
fruit_totals_good = pairs.reduceByKey(lambda a, b: a + b)
fruit_totals_bad  = pairs.groupByKey().mapValues(sum)  # KÖTÜ PRATIK

print("Meyve toplamları (reduceByKey):", fruit_totals_good.collect())

# sortByKey ile sıralama
sorted_fruits = fruit_totals_good.sortByKey(ascending=True)
print("Sıralı:", sorted_fruits.collect())

# countByKey: Eylem – Her anahtar için sayı döner
count_dict = pairs.countByKey()
print("Her anahtarın sayısı:", dict(count_dict))

# ─────────────────────────────────────────────────────────────────────
# 5. Persist / Cache: İteratif Algoritmalar İçin Kritik
# ─────────────────────────────────────────────────────────────────────

from pyspark import StorageLevel

# Büyük veri setini RAM+Disk'e kalıcı sakla
large_rdd = sc.parallelize(range(10_000_000), 16)
large_rdd.persist(StorageLevel.MEMORY_AND_DISK)

# İlk eylem – veri hesaplanıp cache'lenir
t1 = time.time()
print(f"Toplam: {large_rdd.sum():.0f}  ({time.time()-t1:.2f}s – ilk hesaplama)")

# İkinci eylem – cache'den okunur, çok daha hızlı
t2 = time.time()
print(f"Ortalama: {large_rdd.mean():.2f}  ({time.time()-t2:.2f}s – cache'den)")

large_rdd.unpersist()  # Belleği serbest bırak

# ─────────────────────────────────────────────────────────────────────
# 6. Broadcast Değişkenler: Büyük Lookup Tablosunu Her Executor'a Gönder
# ─────────────────────────────────────────────────────────────────────

# Küçük lookup tablosu (örn. ürün kataloğu)
product_names = {1: "Laptop", 2: "Telefon", 3: "Tablet", 4: "Ekran"}

# broadcast: Tüm Executor'lara bir kez gönderilir, tekrar tekrar ağdan çekilmez
broadcast_products = sc.broadcast(product_names)

orders = sc.parallelize([(1, 150), (2, 80), (1, 200), (3, 45), (4, 320)])
enriched = orders.map(
    lambda x: (broadcast_products.value.get(x[0], "Bilinmiyor"), x[1])
)
print("Zenginleştirilmiş siparişler:", enriched.collect())

# ─────────────────────────────────────────────────────────────────────
# 7. Accumulator: Dağıtık Sayaç
# ─────────────────────────────────────────────────────────────────────

error_count = sc.accumulator(0)

def process_line(line):
    global error_count
    if "ERROR" in line:
        error_count.add(1)
    return line

log_lines = sc.parallelize([
    "INFO: User login",
    "ERROR: DB connection failed",
    "INFO: Data processed",
    "ERROR: Timeout occurred",
    "WARN: High memory usage"
])

processed = log_lines.map(process_line)
processed.count()  # Eylemi tetikle
print(f"Toplam hata satırı: {error_count.value}")

sc.stop()
