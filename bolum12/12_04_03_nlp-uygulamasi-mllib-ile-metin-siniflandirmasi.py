# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.4. PySpark ve MLlib ile Dağıtık Makine Öğrenmesi › 12.4.3. Uygulama: Devasa Veri Seti Üzerinde Dağıtık Sınıflandırma › NLP Uygulaması: MLlib ile Metin Sınıflandırması
# Kitap  : Kod 12.10 (MLlib ile metin sınıflandırma)
# Dosya : bolum12/12_04_03_nlp-uygulamasi-mllib-ile-metin-siniflandirmasi.py
# Gerekli: pip install pyspark
# ==========================================================================
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum12/12_04_03_uygulama-*
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .appName("VM-ML Bolum12")
         .master("local[*]")
         .getOrCreate())
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# ─────────────────────────────────────────────────────────────────────
# TF-IDF Pipeline: Metin → Sayısal Özellik → Model
# ─────────────────────────────────────────────────────────────────────

# Örnek metin verisi (gerçekte Kafka'dan veya HDFS'ten okunur)
text_data = [
    (0, "bu ürün çok harika ve kaliteli tavsiye ederim"),
    (1, "kötü ürün hayal kırıklığı yarattı"),
    (0, "mükemmel teslimat hızlı ve güvenilir"),
    (1, "ürün bozuk geldi iade ettim"),
    (0, "fiyat performans açısından çok iyi"),
    (1, "satıcı yanıltıcı reklam yapıyor"),
]
text_df = spark.createDataFrame(text_data, ["label", "metin"])

# NLP Pipeline
tokenizer = Tokenizer(inputCol="metin", outputCol="kelimeler")

remover = StopWordsRemover(
    inputCol="kelimeler",
    outputCol="temiz_kelimeler",
    stopWords=["ve", "bu", "çok", "bir", "da", "de"]
)

# TF: Kelime Frekansı (hashingTF → seyrek vektör)
hashingTF = HashingTF(
    inputCol="temiz_kelimeler",
    outputCol="tf",
    numFeatures=2**15  # 32768 özellik boyutu
)

# IDF: Ters Doküman Frekansı
idf = IDF(inputCol="tf", outputCol="tfidf")

lr_nlp = LogisticRegression(featuresCol="tfidf", labelCol="label", maxIter=10)

nlp_pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr_nlp])
nlp_model = nlp_pipeline.fit(text_df)

# Yeni metinleri sınıflandır
test_texts = [
    (None, "harika bir ürün kesinlikle tavsiye ederim"),
    (None, "çok kötü kalitesiz ürün aldatmaca"),
]
test_text_df = spark.createDataFrame(test_texts, ["label", "metin"])
result = nlp_model.transform(test_text_df)
result.select("metin", "prediction", "probability").show(truncate=False)

spark.stop()
