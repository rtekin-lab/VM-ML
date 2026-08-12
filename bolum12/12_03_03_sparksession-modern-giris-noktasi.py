# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.3. Apache Spark Devrimi: Bellek İçi (In-Memory) Veri İşleme › 12.3.3. Spark DataFrame ve SQL API: Yapılandırılmış Büyük Veri Analizi › SparkSession: Modern Giriş Noktası
# Kitap  : Kod 12.8 (SparkSession ile DataFrame API kullanımı)
# Dosya : bolum12/12_03_03_sparksession-modern-giris-noktasi.py
# Gerekli: pip install pyspark
# ==========================================================================
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.window import Window
import datetime

# ─────────────────────────────────────────────────────────────────────
# 1. SparkSession Oluşturma ve Yapılandırma
# ─────────────────────────────────────────────────────────────────────

spark = (SparkSession.builder
    .appName("DataFrame_Advanced_Demo")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "8")     # Küçük veri için 200'den az
    .config("spark.sql.adaptive.enabled", "true")    # AQE (Adaptive Query Execution)
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# ─────────────────────────────────────────────────────────────────────
# 2. DataFrame Oluşturma Yöntemleri
# ─────────────────────────────────────────────────────────────────────

# Yöntem 1: Python listesinden – küçük test verisi için
data = [
    ("Ayşe",   "Pazarlama", 58000, "İstanbul", 2019),
    ("Mehmet", "Mühendislik", 75000, "Ankara",  2017),
    ("Zeynep", "Pazarlama", 62000, "İzmir",    2020),
    ("Can",    "Mühendislik", 82000, "İstanbul", 2016),
    ("Selin",  "Finans",    69000, "Ankara",   2018),
    ("Burak",  "Mühendislik", 91000, "İstanbul", 2015),
    ("Nisa",   "Finans",    73000, "İzmir",    2017),
]

# Açık şema tanımı – inferSchema'dan daha güvenli
schema = StructType([
    StructField("isim",      StringType(),  nullable=False),
    StructField("departman", StringType(),  nullable=False),
    StructField("maas",      IntegerType(), nullable=False),
    StructField("sehir",     StringType(),  nullable=True),
    StructField("baslama",   IntegerType(), nullable=False),
])

df = spark.createDataFrame(data, schema)

# Yöntem 2: CSV'den – büyük veri için
# df = spark.read.csv("hdfs://cluster/data/calisanlar.csv",
#                     header=True, schema=schema, encoding="UTF-8")

# Yöntem 3: JSON'dan
# df = spark.read.json("s3://bucket/data/logs/*.json")

# Yöntem 4: Parquet'tan (sütunlu format; büyük analizlerde tercih)
# df = spark.read.parquet("hdfs://cluster/data/parquet/")

print(f"DataFrame satır sayısı: {df.count()}")
print(f"Partition sayısı: {df.rdd.getNumPartitions()}")
df.printSchema()
df.show()

# ─────────────────────────────────────────────────────────────────────
# 3. Temel DataFrame İşlemleri
# ─────────────────────────────────────────────────────────────────────

# Sütun seçimi ve yeni sütun ekle
df2 = df.select(
    "isim", "departman", "maas",
    F.col("maas") * 1.15   .alias("maas_artisli"),    # %15 artış
    (2024 - F.col("baslama")).alias("kidem_yili"),
    F.upper(F.col("sehir")).alias("sehir_buyuk"),
)
df2.show()

# Filtreleme
muhendisler = df.filter(
    (F.col("departman") == "Mühendislik") & (F.col("maas") > 80000)
)
print(f"Yüksek maaşlı mühendis: {muhendisler.count()}")

# Gruplama ve Agregasyon
dept_stats = df.groupBy("departman").agg(
    F.count("isim").alias("calisan_sayisi"),
    F.avg("maas").alias("ortalama_maas"),
    F.max("maas").alias("max_maas"),
    F.min("maas").alias("min_maas"),
    F.stddev("maas").alias("maas_std"),
).orderBy("ortalama_maas", ascending=False)
dept_stats.show()

# ─────────────────────────────────────────────────────────────────────
# 4. Window Fonksiyonları (Analitik Fonksiyonlar)
# ─────────────────────────────────────────────────────────────────────

# Departman içinde maaşa göre sıralama
window_spec = Window.partitionBy("departman").orderBy(F.col("maas").desc())

df_ranked = df.withColumn(
    "dept_ici_siralama",
    F.rank().over(window_spec)
).withColumn(
    "dept_ici_maas_payi",
    (F.col("maas") / F.sum("maas").over(Window.partitionBy("departman")) * 100).cast("int"),
)
df_ranked.select("isim", "departman", "maas", "dept_ici_siralama", "dept_ici_maas_payi").show()

# ─────────────────────────────────────────────────────────────────────
# 5. SQL Sorguları
# ─────────────────────────────────────────────────────────────────────

df.createOrReplaceTempView("calisanlar")

result = spark.sql("""
    SELECT
        departman,
        COUNT(*) as calisan,
        ROUND(AVG(maas), 2) as ort_maas,
        MAX(maas) - MIN(maas) as maas_araliği
    FROM calisanlar
    WHERE baslama >= 2016
    GROUP BY departman
    HAVING COUNT(*) >= 2
    ORDER BY ort_maas DESC
""")
result.show()

# ─────────────────────────────────────────────────────────────────────
# 6. Parquet Formatında Kaydetme (Sütunlu depolama; büyük analitik)
# ─────────────────────────────────────────────────────────────────────

# Partition'lı yazma – departmana göre klasör yapısı oluşturur
# df.write.partitionBy("departman").parquet("output/calisanlar_parquet")

# Parquet okuma – yalnızca ilgili partition'lar okunur (partition pruning)
# df_parquet = spark.read.parquet("output/calisanlar_parquet")
# df_parquet.filter(F.col("departman") == "Mühendislik").show()

spark.stop()
