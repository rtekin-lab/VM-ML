# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.4. PySpark ve MLlib ile Dağıtık Makine Öğrenmesi › 12.4.3. Uygulama: Devasa Veri Seti Üzerinde Dağıtık Sınıflandırma
# Kitap  : Kod 12.9 (MLlib ile dağıtık sınıflandırma boru hattı)
# Dosya : bolum12/12_04_03_uygulama-devasa-veri-seti-uzerinde-dagitik-sinif.py
# Gerekli: pip install numpy pyspark
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
                               IntegerType, DoubleType, FloatType)
spark = (SparkSession.builder
         .appName("VM-ML Bolum12")
         .master("local[*]")
         .getOrCreate())
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler,
    StandardScaler, PCA, ChiSqSelector, Word2Vec
)
from pyspark.ml.classification import (
    LogisticRegression, RandomForestClassifier,
    GBTClassifier, LinearSVC
)
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.clustering import KMeans, BisectingKMeans
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator, MulticlassClassificationEvaluator
)
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
import numpy as np

# ─────────────────────────────────────────────────────────────────────
# 1. SparkSession Başlatma (Büyük Küme Yapılandırması)
# ─────────────────────────────────────────────────────────────────────

spark = (SparkSession.builder
    .appName("Distributed_ML_Complete")
    .master("local[*]")  # Üretimde: yarn veya k8s
    .config("spark.executor.memory", "4g")
    .config("spark.executor.cores", "4")
    .config("spark.driver.memory", "2g")
    .config("spark.sql.shuffle.partitions", "50")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.ml.linalg.vectorSize", "2048")
    .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# ─────────────────────────────────────────────────────────────────────
# 2. Sentetik Büyük Veri Oluşturma (Gerçekte HDFS/S3'ten okunur)
# ─────────────────────────────────────────────────────────────────────

import random
n_records = 100_000

# Müşteri tıklama davranışı simülasyonu
schema = StructType([
    StructField("user_id",      IntegerType(), False),
    StructField("age",          IntegerType(), True),
    StructField("gender",       StringType(),  True),
    StructField("kategori",     StringType(),  True),
    StructField("sayfa_goruntuleme", IntegerType(), True),
    StructField("oturum_suresi",DoubleType(),  True),
    StructField("onceki_satin_alma", IntegerType(), True),
    StructField("sehir",        StringType(),  True),
    StructField("cihaz",        StringType(),  True),
    StructField("clicked",      IntegerType(), False),   # Hedef değişken
])

kategoriler = ["Elektronik", "Giyim", "Spor", "Kitap", "Kozmetik"]
sehirler    = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"]
cihazlar    = ["mobile", "desktop", "tablet"]

rows = []
for i in range(n_records):
    yas   = random.randint(18, 65)
    cinsiyet = random.choice(["M", "F"])
    kat   = random.choice(kategoriler)
    pgv   = random.randint(1, 50)
    sure  = round(random.uniform(10, 3600), 1)
    onceki= random.randint(0, 20)
    sehir = random.choice(sehirler)
    cihaz = random.choice(cihazlar)
    # Basit kural: genç + mobil + çok sayfa görüntüleme = yüksek tıklama olasılığı
    prob  = (yas < 35) * 0.3 + (cihaz == "mobile") * 0.2 + min(pgv/50, 0.3) + 0.1
    clicked = 1 if random.random() < prob else 0
    rows.append((i, yas, cinsiyet, kat, pgv, sure, onceki, sehir, cihaz, clicked))

df_raw = spark.createDataFrame(rows, schema)
print(f"Toplam kayıt: {df_raw.count():,}")
print(f"Tıklanma oranı: {df_raw.filter(F.col('clicked')==1).count()/n_records:.2%}")

# ─────────────────────────────────────────────────────────────────────
# 3. Keşifsel Veri Analizi (EDA)
# ─────────────────────────────────────────────────────────────────────

print("\n=== Kategorik Dağılım ===")
df_raw.groupBy("kategori").agg(
    F.count("*").alias("toplam"),
    F.mean("clicked").alias("ort_tiklanma"),
    F.mean("oturum_suresi").alias("ort_sure")
).orderBy("ort_tiklanma", ascending=False).show()

print("\n=== Sayısal İstatistikler ===")
df_raw.select("age", "sayfa_goruntuleme", "oturum_suresi", "onceki_satin_alma").describe().show()

# ─────────────────────────────────────────────────────────────────────
# 4. Özellik Mühendisliği
# ─────────────────────────────────────────────────────────────────────

# Yeni özellikler türet
df_featured = df_raw.withColumn(
    "sayfa_sure_orani",
    F.col("sayfa_goruntuleme") / (F.col("oturum_suresi") / 60 + 1)
).withColumn(
    "toplam_ilgi",
    F.col("sayfa_goruntuleme") * F.col("oturum_suresi") / 1000
).withColumn(
    "yas_grubu",
    F.when(F.col("age") < 25, "genc")
     .when(F.col("age") < 40, "orta")
     .otherwise("yasli"),
)

# ─────────────────────────────────────────────────────────────────────
# 5. Eksik Veri Yönetimi (Büyük Veri Ortamında)
# ─────────────────────────────────────────────────────────────────────

# Eksik değerleri sütun ortalaması ile doldur
numeric_cols = ["age", "sayfa_goruntuleme", "oturum_suresi", "onceki_satin_alma"]
fill_means = {col: df_featured.select(F.mean(col)).first()[0]
              for col in numeric_cols}
df_clean = df_featured.fillna(fill_means)
df_clean = df_clean.fillna({"gender": "Bilinmiyor", "sehir": "Diger"})

# ─────────────────────────────────────────────────────────────────────
# 6. Pipeline Aşamaları Tanımla
# ─────────────────────────────────────────────────────────────────────

# 6a. Kategorik değişkenleri sayısala çevir
cat_cols = ["gender", "kategori", "sehir", "cihaz", "yas_grubu"]
indexed_cols = [f"{c}_idx" for c in cat_cols]
encoded_cols = [f"{c}_ohe" for c in cat_cols]

indexers = [
    StringIndexer(inputCol=c, outputCol=ic, handleInvalid="keep")
    for c, ic in zip(cat_cols, indexed_cols)
]

encoders = [
    OneHotEncoder(inputCol=ic, outputCol=ec, dropLast=True)
    for ic, ec in zip(indexed_cols, encoded_cols)
]

# 6b. Tüm özellikleri tek vektörde topla
num_cols = [
    "age", "sayfa_goruntuleme", "oturum_suresi", "onceki_satin_alma",
    "sayfa_sure_orani", "toplam_ilgi"
]
all_feature_cols = num_cols + encoded_cols

assembler = VectorAssembler(
    inputCols=all_feature_cols,
    outputCol="raw_features",
    handleInvalid="keep"
)

# 6c. Standardizasyon
scaler = StandardScaler(
    inputCol="raw_features",
    outputCol="scaled_features",
    withMean=True,
    withStd=True
)

# 6d. PCA ile boyut azaltma (isteğe bağlı)
pca = PCA(k=10, inputCol="scaled_features", outputCol="pca_features")

# ─────────────────────────────────────────────────────────────────────
# 7. Hedef Değişkeni Hazırla
# ─────────────────────────────────────────────────────────────────────

label_indexer = StringIndexer(inputCol="clicked", outputCol="label")

# ─────────────────────────────────────────────────────────────────────
# 8. Eğitim/Test Bölme
# ─────────────────────────────────────────────────────────────────────

train_df, test_df = df_clean.randomSplit([0.8, 0.2], seed=42)
train_df.cache()  # İteratif algoritma için cache et

print(f"Eğitim: {train_df.count():,}  |  Test: {test_df.count():,}")

# ─────────────────────────────────────────────────────────────────────
# 9. Model 1: Lojistik Regresyon Pipeline
# ─────────────────────────────────────────────────────────────────────

lr = LogisticRegression(
    featuresCol="scaled_features",
    labelCol="clicked",
    maxIter=20,
    regParam=0.01,      # L2 regularizasyon
    elasticNetParam=0.0 # 0=L2, 1=L1
)

lr_pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, lr])

import time
start = time.time()
lr_model = lr_pipeline.fit(train_df)
print(f"Lojistik Regresyon eğitim süresi: {time.time()-start:.1f}s")

# Değerlendirme
lr_preds = lr_model.transform(test_df)
evaluator_bin = BinaryClassificationEvaluator(
    labelCol="clicked", metricName="areaUnderROC")
evaluator_acc = MulticlassClassificationEvaluator(
    labelCol="clicked", predictionCol="prediction", metricName="accuracy")

lr_auc = evaluator_bin.evaluate(lr_preds)
lr_acc = evaluator_acc.evaluate(lr_preds)
print(f"Lojistik Regresyon – AUC: {lr_auc:.4f}  |  Accuracy: {lr_acc:.4f}")

# ─────────────────────────────────────────────────────────────────────
# 10. Model 2: Random Forest
# ─────────────────────────────────────────────────────────────────────

rf = RandomForestClassifier(
    featuresCol="scaled_features",
    labelCol="clicked",
    numTrees=50,
    maxDepth=8,
    seed=42
)

rf_pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, rf])

start = time.time()
rf_model = rf_pipeline.fit(train_df)
print(f"Random Forest eğitim süresi: {time.time()-start:.1f}s")

rf_preds = rf_model.transform(test_df)
rf_auc   = evaluator_bin.evaluate(rf_preds)
rf_acc   = evaluator_acc.evaluate(rf_preds)
print(f"Random Forest – AUC: {rf_auc:.4f}  |  Accuracy: {rf_acc:.4f}")

# Özellik Önem Skoru
rf_fit  = rf_model.stages[-1]
importances = rf_fit.featureImportances
print(f"En önemli özellik indeksleri (ilk 5): {importances.indices[:5].tolist()}")

# ─────────────────────────────────────────────────────────────────────
# 11. Hiperparametre Araması: CrossValidator
# ─────────────────────────────────────────────────────────────────────

lr_cv = LogisticRegression(featuresCol="scaled_features", labelCol="clicked")
cv_pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, lr_cv])

param_grid = (ParamGridBuilder()
    .addGrid(lr_cv.maxIter,   [10, 20])
    .addGrid(lr_cv.regParam,  [0.001, 0.01, 0.1])
    .addGrid(lr_cv.elasticNetParam, [0.0, 0.5])
    .build())
print(f"Test edilecek kombinasyon sayısı: {len(param_grid)} (2×3×2 = 12)")

cv = CrossValidator(
    estimator=cv_pipeline,
    estimatorParamMaps=param_grid,
    evaluator=BinaryClassificationEvaluator(labelCol="clicked"),
    numFolds=3,
    seed=42,
    parallelism=4   # Aynı anda 4 kombinasyonu paralel test et
)

print("CrossValidator çalışıyor (dağıtık hiperparametre araması)...")
start = time.time()
cv_model = cv.fit(train_df)
print(f"CrossValidator süresi: {time.time()-start:.1f}s")

cv_preds = cv_model.transform(test_df)
cv_auc   = evaluator_bin.evaluate(cv_preds)
print(f"En iyi model AUC: {cv_auc:.4f}")

# En iyi parametreler
best_lr = cv_model.bestModel.stages[-1]
print(f"En iyi maxIter: {best_lr.getMaxIter()}")
print(f"En iyi regParam: {best_lr.getRegParam()}")

# ─────────────────────────────────────────────────────────────────────
# 12. K-Means Kümeleme (Gözetimsiz)
# ─────────────────────────────────────────────────────────────────────

kmeans = KMeans(featuresCol="scaled_features", k=4, seed=42, maxIter=20)
km_pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, kmeans])
km_model = km_pipeline.fit(df_clean)
km_preds = km_model.transform(df_clean)

# Küme profili
km_preds.groupBy("prediction").agg(
    F.count("*").alias("kume_boyutu"),
    F.mean("age").alias("ort_yas"),
    F.mean("clicked").alias("tiklanma_orani"),
    F.mean("oturum_suresi").alias("ort_sure")
).orderBy("kume_boyutu", ascending=False).show()

# Küme içi varyans toplamı (WSSSE)
wssse = km_model.stages[-1].summary.trainingCost
print(f"K-Means WSSSE (küme kalitesi): {wssse:,.2f}")

# ─────────────────────────────────────────────────────────────────────
# 13. ALS ile Öneri Sistemi
# ─────────────────────────────────────────────────────────────────────

# Kullanıcı-ürün etkileşim matrisi simülasyonu
ratings_data = [(int(i % 1000), int(j), float(random.randint(1, 5)))
                for i in range(10000)
                for j in random.sample(range(500), 5)]

ratings_schema = StructType([
    StructField("userId",    IntegerType(), False),
    StructField("productId", IntegerType(), False),
    StructField("rating",    FloatType(),   False),
])

ratings_df = spark.createDataFrame(ratings_data, ratings_schema)

als = ALS(
    maxIter=10,
    regParam=0.1,
    rank=20,
    userCol="userId",
    itemCol="productId",
    ratingCol="rating",
    coldStartStrategy="drop"  # Yeni kullanıcı/ürün için NaN önle
)

train_r, test_r = ratings_df.randomSplit([0.8, 0.2])
als_model = als.fit(train_r)
als_preds = als_model.transform(test_r)

from pyspark.ml.evaluation import RegressionEvaluator
rmse = RegressionEvaluator(metricName="rmse", labelCol="rating",
                            predictionCol="prediction").evaluate(als_preds)
print(f"ALS RMSE: {rmse:.4f}")

# Kullanıcı 1 için en iyi 10 öneri
user_recs = als_model.recommendForAllUsers(10)
user_recs.filter(F.col("userId") == 1).show(truncate=False)

# ─────────────────────────────────────────────────────────────────────
# 14. Model Kaydetme ve Yükleme
# ─────────────────────────────────────────────────────────────────────

# Tüm pipeline'ı HDFS veya yerel diske kaydet
# rf_model.write().overwrite().save("hdfs://cluster/models/rf_ctr_model")
rf_model.write().overwrite().save(os.path.join(tempfile.gettempdir(), "rf_ctr_model"))
print("Model /tmp/rf_ctr_model konumuna kaydedildi.")

# Modeli geri yükle (başka bir Spark uygulamasında)
from pyspark.ml import PipelineModel
loaded_model = PipelineModel.load(os.path.join(tempfile.gettempdir(), "rf_ctr_model"))

# Yeni veriler üzerinde tahmin
new_preds = loaded_model.transform(test_df)
print(f"Yüklenen model AUC: {evaluator_bin.evaluate(new_preds):.4f}")

train_df.unpersist()
spark.stop()
