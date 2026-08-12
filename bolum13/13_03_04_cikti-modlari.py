# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.3. Apache Flink ile Gerçek Zamanlı Veri İşleme Motoru › 13.3.4. Alternatif Motor: Spark Structured Streaming ile Akış İşleme › Çıktı Modları (Output Modes)
# Dosya : bolum13/13_03_04_cikti-modlari.py
# Gerekli: pip install pyspark
# ==========================================================================
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: PySpark tip tanımları
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType, StructField, StringType,
                               IntegerType, DoubleType)
spark = (SparkSession.builder
         .appName("VM-ML Bolum13")
         .master("local[*]")
         .getOrCreate())
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import json

spark = (SparkSession.builder
    .appName("KafkaStructuredStreaming")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# ─────────────────────────────────────────────────────────────────────
# 1. Kafka'dan Akan Veri Okuma
# ─────────────────────────────────────────────────────────────────────

kafka_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "finansal-islemler")   # Çoklu: "topic1,topic2"
    .option("startingOffsets", "latest")         # "earliest" veya JSON offset
    .option("failOnDataLoss", "false")
    .option("maxOffsetsPerTrigger", 10000)        # Mikro-batch başına max mesaj
    .load())

# Kafka'dan gelen raw DataFrame şeması: key, value, topic, partition, offset, timestamp
kafka_df.printSchema()

# ─────────────────────────────────────────────────────────────────────
# 2. Mesaj Deserializasyonu
# ─────────────────────────────────────────────────────────────────────

txn_schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("user_id",        StringType()),
    StructField("amount",         DoubleType()),
    StructField("merchant",       StringType()),
    StructField("country",        StringType()),
    StructField("timestamp",      StringType()),
    StructField("card_type",      StringType()),
])

# JSON mesajı parse et
parsed_df = (kafka_df
    .select(F.from_json(F.col("value").cast("string"), txn_schema).alias("data"),
            F.col("timestamp").alias("kafka_ts"))
    .select("data.*", "kafka_ts")
    .withColumn("event_time",
                F.to_timestamp(F.col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))
)

# ─────────────────────────────────────────────────────────────────────
# 3. Pencere Tabanlı Gerçek Zamanlı Aggregasyon
# ─────────────────────────────────────────────────────────────────────

# Watermark: 10 dakikaya kadar geç gelen verileri kabul et
windowed_agg = (parsed_df
    .withWatermark("event_time", "10 minutes")
    .groupBy(
        F.window(F.col("event_time"), "5 minutes"),   # 5 dakikalık pencere
        F.col("merchant")
    ).agg(
        F.count("transaction_id").alias("islem_sayisi"),
        F.sum("amount").alias("toplam_tutar"),
        F.avg("amount").alias("ort_tutar"),
        F.max("amount").alias("max_tutar"),
    ).orderBy("toplam_tutar", ascending=False)
)

# ─────────────────────────────────────────────────────────────────────
# 4. Gerçek Zamanlı Anomali Tespiti (UDF ile)
# ─────────────────────────────────────────────────────────────────────

# Kullanıcı başına 5 dakikadaki toplam harcama
user_window_agg = (parsed_df
    .withWatermark("event_time", "5 minutes")
    .groupBy(
        F.window(F.col("event_time"), "5 minutes", "1 minute"),  # Kayan pencere
        F.col("user_id")
    ).agg(
        F.sum("amount").alias("pencere_toplam"),
        F.count("*").alias("islem_adedi"),
    ).filter(F.col("pencere_toplam") > 3000)  # 5 dk'da 3000 TL üzeri uyarı
)

# ─────────────────────────────────────────────────────────────────────
# 5. ML Modeli ile Gerçek Zamanlı Sınıflandırma
# ─────────────────────────────────────────────────────────────────────

from pyspark.ml import PipelineModel

# Önceden eğitilmiş fraud detection modelini yükle
# fraud_model = PipelineModel.load("hdfs://cluster/models/fraud_detector_v3")

# Her mikro-batch'e model uygula (foreachBatch)
def process_batch(batch_df, batch_id):
    """Her mikro-batch üzerinde ML tahmini ve kayıt."""
    if batch_df.isEmpty():
        return
    print(f"Batch {batch_id}: {batch_df.count()} işlem işleniyor")
    # predictions = fraud_model.transform(batch_df)
    # predictions.filter(F.col("prediction") == 1) \
    #     .write.format("kafka") \
    #     .option("kafka.bootstrap.servers", "localhost:9092") \
    #     .option("topic", "fraud-alerts") \
    #     .save()
    batch_df.show(5)

# ─────────────────────────────────────────────────────────────────────
# 6. Sorguyu Başlatma ve Çıktı Yazma
# ─────────────────────────────────────────────────────────────────────

# Konsola yaz (geliştirme/test)
console_query = (windowed_agg.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", "false")
    .trigger(processingTime="10 seconds")  # Her 10 saniyede bir mikro-batch
    .start())

# Parquet'a yaz (üretim)
# parquet_query = (windowed_agg.writeStream
#     .outputMode("append")
#     .format("parquet")
#     .option("path", "hdfs://cluster/streaming/merchant_stats")
#     .option("checkpointLocation", "hdfs://cluster/checkpoints/merchant_stats")
#     .trigger(processingTime="1 minute")
#     .start())

# foreachBatch ile ML model uygulama
ml_query = (parsed_df.writeStream
    .foreachBatch(process_batch)
    .option("checkpointLocation", os.path.join(tempfile.gettempdir(), "checkpoints/fraud"))
    .trigger(processingTime="5 seconds")
    .start())

# Tüm sorguları bekle
spark.streams.awaitAnyTermination(timeout=60)
spark.stop()
