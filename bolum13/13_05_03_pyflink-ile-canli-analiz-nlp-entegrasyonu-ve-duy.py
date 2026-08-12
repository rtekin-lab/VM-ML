# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.5. Uçtan Uca Vaka Çalışması (Case Study): › 13.5.3. PyFlink ile Canlı Analiz: NLP Entegrasyonu ve Duygu Analizi Pipeline'ı
# Dosya : bolum13/13_05_03_pyflink-ile-canli-analiz-nlp-entegrasyonu-ve-duy.py
# Gerekli: pip install apache-flink kafka-python nltk transformers
# ==========================================================================
# ================================================================
# PyFlink Gerçek Zamanlı Sentiment Analysis Pipeline
# pip install apache-flink kafka-python nltk transformers torch
# ================================================================
import json, time, re, logging
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import (
    MapFunction, FilterFunction, FlatMapFunction,
    AggregateFunction, ProcessWindowFunction
)
from pyflink.datastream.window import TumblingEventTimeWindows, SlidingEventTimeWindows
from pyflink.common.time import Time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SentimentPipeline')

# ================================================================
# KATMAN 1: Ön İşleme
# ================================================================
class TweetPreprocessor(MapFunction):
    """
    Tweet metnini NLP modellerine hazırlar.
    Akış içinde her olay için O(len(text)) karmaşıklıkta çalışır.
    """
    URL_PATTERN     = re.compile(r'http\S+|www\.\S+')
    MENTION_PATTERN = re.compile(r'@\w+')
    EMOJI_PATTERN   = re.compile(
        '[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
        '\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+',
        flags=re.UNICODE
    )

    def map(self, value: str) -> str:
        try:
            tweet = json.loads(value)
            text = tweet.get('text', '')

            # Temizleme zinciri
            text = self.URL_PATTERN.sub('', text)
            text = self.MENTION_PATTERN.sub('', text)
            # Emoji'leri koru (VADER emoji'lerden anlam çıkarır)
            text = re.sub(r'\s+', ' ', text).strip()

            tweet['processed_text'] = text
            tweet['char_count']     = len(text)
            tweet['word_count']     = len(text.split())
            return json.dumps(tweet, ensure_ascii=False)
        except Exception as e:
            logger.warning(f'Önişleme hatası: {e}')
            return value  # Hatalı kayıtlar değişmeden geçsin

class ValidTweetFilter(FilterFunction):
    """Kısa, boş veya dil dışı tweet'leri elee."""
    MIN_WORDS = 3
    ALLOWED_LANGS = {'en', 'tr'}

    def filter(self, value: str) -> bool:
        try:
            tweet = json.loads(value)
            text  = tweet.get('processed_text', '')
            lang  = tweet.get('lang', 'und')
            return (
                lang in self.ALLOWED_LANGS and
                len(text.split()) >= self.MIN_WORDS
            )
        except Exception:
            return False

# ================================================================
# KATMAN 2: Duygu Analizi (VADER birincil + DistilBERT ikincil)
# ================================================================
class HybridSentimentAnalyzer(MapFunction):
    """
    İki aşamalı hibrit NLP sistemi.
    VADER hızlı ama yüzeysel; DistilBERT yavaş ama derin.
    Güven eşiğine göre hangi modelin kullanılacağı karar verilir.
    """
    VADER_CONFIDENCE_THRESHOLD = 0.5   # Bu değer üstünde VADER'a güven
    BERT_MODEL_NAME = 'distilbert-base-uncased-finetuned-sst-2-english'

    def open(self, runtime_context):
        # VADER'ı başlat (senkron, hızlı)
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        self.vader = SentimentIntensityAnalyzer()

        # DistilBERT'i başlat (asenkron yükleme, zaman alır)
        try:
            from transformers import pipeline as hf_pipeline
            self.bert_pipeline = hf_pipeline(
                'sentiment-analysis',
                model=self.BERT_MODEL_NAME,
                device=-1,     # -1: CPU, 0: GPU (varsa)
                truncation=True,
                max_length=128  # Tweet'ler genelde kısadır
            )
            self.bert_available = True
            logger.info('DistilBERT başarıyla yüklendi.')
        except Exception as e:
            logger.warning(f'DistilBERT yüklenemedi, yalnızca VADER kullanılacak: {e}')
            self.bert_available = False

    def _vader_analyze(self, text: str) -> dict:
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        label = ('POSITIVE' if compound >= 0.05
                 else 'NEGATIVE' if compound <= -0.05
                 else 'NEUTRAL')
        confidence = abs(compound)
        return {
            'vader_compound': compound,
            'vader_pos':      scores['pos'],
            'vader_neg':      scores['neg'],
            'vader_neu':      scores['neu'],
            'vader_label':    label,
            'vader_confidence': confidence
        }

    def _bert_analyze(self, text: str) -> dict:
        try:
            result = self.bert_pipeline(text[:512])[0]  # Truncate
            label  = result['label']  # 'POSITIVE' or 'NEGATIVE'
            score  = result['score']  # [0, 1]
            return {
                'bert_label':  label,
                'bert_score':  score,
                'bert_compound': score if label == 'POSITIVE' else -score
            }
        except Exception as e:
            return {'bert_label': 'NEUTRAL', 'bert_score': 0.5, 'bert_compound': 0.0}

    def map(self, value: str) -> str:
        try:
            tweet = json.loads(value)
            text  = tweet.get('processed_text', '')

            # Aşama 1: VADER analizi
            vader_result = self._vader_analyze(text)
            tweet.update(vader_result)

            # Aşama 2: Düşük güven → DistilBERT'e yönlendir
            used_bert = False
            if (self.bert_available and
                    vader_result['vader_confidence'] < self.VADER_CONFIDENCE_THRESHOLD):
                bert_result = self._bert_analyze(text)
                tweet.update(bert_result)
                used_bert = True

                # Hibrit skor: 0.35 * VADER + 0.65 * BERT
                final_compound = (
                    0.35 * vader_result['vader_compound'] +
                    0.65 * bert_result['bert_compound']
                )
            else:
                final_compound = vader_result['vader_compound']

            # Final sınıflandırma
            tweet['final_compound'] = round(final_compound, 4)
            tweet['final_label'] = (
                'POSITIVE' if final_compound >= 0.05
                else 'NEGATIVE' if final_compound <= -0.05
                else 'NEUTRAL'
            )
            tweet['used_bert']   = used_bert
            tweet['analyzed_at'] = time.time()

            return json.dumps(tweet, ensure_ascii=False)
        except Exception as e:
            logger.error(f'Sentiment analiz hatası: {e}')
            return value

# ================================================================
# KATMAN 3: Hashtag Çıkarıcı (FlatMap — Bire-Çok)
# ================================================================
class HashtagExpander(FlatMapFunction):
    """
    Her tweet için, içerdiği hashtag başına bir kayıt üretir.
    Bu, hashtag bazında aggregation yapabilmek için gereklidir.
    Bire-Çok (FlatMap) dönüşümü: 1 tweet → N hashtag kaydı
    """
    def flat_map(self, value: str):
        try:
            tweet = json.loads(value)
            hashtags = tweet.get('hashtags', [])

            if not hashtags:
                # Hashtag yoksa '#general' olarak etiketle
                record = dict(tweet)
                record['hashtag_key'] = '_general'
                yield json.dumps(record)
                return

            for tag in hashtags:
                record = dict(tweet)
                record['hashtag_key'] = tag.lower()
                yield json.dumps(record)
        except Exception:
            yield value

# ================================================================
# KATMAN 4: Pencere Tabanlı Hashtag Duygu Agregasyonu
# ================================================================
class SentimentAccumulator:
    """Pencere içindeki duygu istatistiklerini tutar."""
    __slots__ = ['count', 'pos', 'neg', 'neu', 'sum_compound',
                 'sum_likes', 'sum_rts']
    def __init__(self):
        self.count       = 0
        self.pos         = 0
        self.neg         = 0
        self.neu         = 0
        self.sum_compound = 0.0
        self.sum_likes   = 0
        self.sum_rts     = 0

class HashtagSentimentAggregator(AggregateFunction):
    """
    Kayan/Atlamalı pencerede hashtag bazında duygu istatistikleri:
    - Ortalama duygu skoru (mean compound)
    - Duygu dağılımı (pos/neg/neu yüzdeleri)
    - Etkileşim ağırlıklı skor (engagement-weighted)
    """
    def create_accumulator(self):
        return SentimentAccumulator()

    def add(self, value: str, acc: SentimentAccumulator):
        try:
            tweet = json.loads(value)
            label = tweet.get('final_label', 'NEUTRAL')
            acc.count += 1
            acc.sum_compound += tweet.get('final_compound', 0.0)
            acc.sum_likes    += tweet.get('like_count', 0)
            acc.sum_rts      += tweet.get('retweet_count', 0)
            if label == 'POSITIVE': acc.pos += 1
            elif label == 'NEGATIVE': acc.neg += 1
            else: acc.neu += 1
        except Exception:
            pass
        return acc

    def get_result(self, acc: SentimentAccumulator) -> str:
        n = max(acc.count, 1)
        mean_compound = acc.sum_compound / n
        # Etkileşim ağırlıklı skor:
        # engagement = log(1 + likes + 3*retweets)  [RT daha değerli]
        import math
        engagement_weight = math.log1p(acc.sum_likes + 3 * acc.sum_rts)
        weighted_score    = mean_compound * (1 + 0.1 * engagement_weight)
        return json.dumps({
            'tweet_count':        acc.count,
            'mean_compound':      round(mean_compound, 4),
            'engagement_score':   round(min(weighted_score, 1.0), 4),
            'positive_pct':       round(acc.pos / n * 100, 1),
            'negative_pct':       round(acc.neg / n * 100, 1),
            'neutral_pct':        round(acc.neu / n * 100, 1),
            'total_likes':        acc.sum_likes,
            'total_retweets':     acc.sum_rts,
            'dominant_sentiment': ('POSITIVE' if acc.pos >= acc.neg and acc.pos >= acc.neu
                                   else 'NEGATIVE' if acc.neg >= acc.pos and acc.neg >= acc.neu
                                   else 'NEUTRAL')
        })

    def merge(self, acc1: SentimentAccumulator, acc2: SentimentAccumulator):
        acc1.count        += acc2.count
        acc1.pos          += acc2.pos
        acc1.neg          += acc2.neg
        acc1.neu          += acc2.neu
        acc1.sum_compound += acc2.sum_compound
        acc1.sum_likes    += acc2.sum_likes
        acc1.sum_rts      += acc2.sum_rts
        return acc1

class WindowedResultEnricher(ProcessWindowFunction):
    """Pencere metadata'sını sonuca ekler."""
    def process(self, key, context, elements, out):
        for agg_json in elements:
            agg = json.loads(agg_json)
            agg['hashtag']      = key
            agg['window_start'] = context.window().start // 1000  # ms → saniye
            agg['window_end']   = context.window().end   // 1000
            agg['window_size']  = '5min_tumbling'
            out.collect(json.dumps(agg))

# ================================================================
# MAIN: Pipeline Tanımı ve Çalıştırma
# ================================================================
def build_sentiment_pipeline(
    kafka_servers: str = 'localhost:9092',
    source_topic:  str = 'tweet_stream',
    result_topic:  str = 'sentiment_results',
    aggreg_topic:  str = 'hashtag_aggregations',
    parallelism:   int = 4,
    checkpoint_interval_ms: int = 30_000
):
    # --- Flink Ortamı ---
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_parallelism(parallelism)
    env.enable_checkpointing(checkpoint_interval_ms)

    # --- Kafka Source ---
    kafka_props = {
        'bootstrap.servers': kafka_servers,
        'group.id':          'flink_sentiment_group'
    }
    kafka_source = FlinkKafkaConsumer(
        topics=source_topic,
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    kafka_source.set_start_from_latest()

    # --- Pipeline Zinciri ---
    raw_stream = env.add_source(kafka_source)

    # Ön işleme ve filtreleme
    clean_stream = (
        raw_stream
        .map(TweetPreprocessor(), output_type=Types.STRING())
        .filter(ValidTweetFilter())
    )

    # Duygu analizi (her tweet için bireysel skor)
    analyzed_stream = clean_stream.map(
        HybridSentimentAnalyzer(), output_type=Types.STRING()
    )

    # Bireysel sonuçları Kafka'ya yaz
    analyzed_stream.add_sink(FlinkKafkaProducer(
        topic=result_topic,
        serialization_schema=SimpleStringSchema(),
        producer_config={'bootstrap.servers': kafka_servers}
    ))

    # Hashtag bazında 5 dakikalık atlamalı pencere agregasyonu
    hashtag_agg = (
        analyzed_stream
        .flat_map(HashtagExpander(), output_type=Types.STRING())
        .key_by(lambda x: json.loads(x).get('hashtag_key', '_general'))
        .window(TumblingEventTimeWindows.of(Time.minutes(5)))
        .aggregate(
            HashtagSentimentAggregator(),
            window_function=WindowedResultEnricher(),
            accumulator_type=Types.STRING(),
            output_type=Types.STRING()
        )
    )

    hashtag_agg.add_sink(FlinkKafkaProducer(
        topic=aggreg_topic,
        serialization_schema=SimpleStringSchema(),
        producer_config={'bootstrap.servers': kafka_servers}
    ))

    # Konsola yazdır (debug için)
    analyzed_stream.print()

    logger.info('PyFlink Sentiment Pipeline baslatiliyor...')
    env.execute('Twitter_Realtime_Sentiment_Analysis')

if __name__ == '__main__':
    build_sentiment_pipeline()

# ================================================================
# Elasticsearch Sink — Flink sonuçlarını ES'e yaz
# pip install elasticsearch
# ================================================================
from elasticsearch import Elasticsearch, helpers
from kafka import KafkaConsumer
import json, time, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ESSink')

# Elasticsearch Index Mapping (Kibana için optimize edilmiş)
TWEET_MAPPING = {
    'mappings': {
        'properties': {
            'tweet_id':       {'type': 'keyword'},
            'text':           {'type': 'text', 'analyzer': 'english'},
            'processed_text': {'type': 'text', 'analyzer': 'english'},
            'lang':           {'type': 'keyword'},
            'hashtags':       {'type': 'keyword'},
            'final_compound': {'type': 'float'},
            'final_label':    {'type': 'keyword'},
            'vader_compound': {'type': 'float'},
            'used_bert':      {'type': 'boolean'},
            'like_count':     {'type': 'integer'},
            'retweet_count':  {'type': 'integer'},
            # Kibana için timestamp alanları
            'created_at':     {'type': 'date'},
            'analyzed_at':    {'type': 'date', 'format': 'epoch_second'}
        }
    },
    'settings': {
        'number_of_shards':   3,   # Kafka partition sayısıyla eşleştir
        'number_of_replicas': 1,
        'refresh_interval':   '5s'  # Gerçek zamanlı görünürlük
    }
}

HASHTAG_MAPPING = {
    'mappings': {
        'properties': {
            'hashtag':           {'type': 'keyword'},
            'tweet_count':       {'type': 'integer'},
            'mean_compound':     {'type': 'float'},
            'engagement_score':  {'type': 'float'},
            'positive_pct':      {'type': 'float'},
            'negative_pct':      {'type': 'float'},
            'dominant_sentiment':{'type': 'keyword'},
            'window_start':      {'type': 'date', 'format': 'epoch_second'},
            'window_end':        {'type': 'date', 'format': 'epoch_second'},
        }
    }
}

class ElasticsearchSink:
    def __init__(self, hosts: list = ['http://localhost:9200']):
        self.es = Elasticsearch(hosts)
        self._ensure_indices()
        self.buffer = []
        self.BUFFER_SIZE = 100  # Her 100 belgede toplu yaz (bulk insert)

    def _ensure_indices(self):
        for idx, mapping in [('tweets', TWEET_MAPPING), ('hashtag_trends', HASHTAG_MAPPING)]:
            if not self.es.indices.exists(index=idx):
                self.es.indices.create(index=idx, body=mapping)
                logger.info(f'Elasticsearch index oluşturuldu: {idx}')

    def index_tweet(self, tweet: dict):
        self.buffer.append({
            '_index': 'tweets',
            '_id':     tweet.get('tweet_id'),
            '_source': tweet
        })
        if len(self.buffer) >= self.BUFFER_SIZE:
            self.flush()

    def index_aggregation(self, agg: dict):
        doc_id = f"{agg['hashtag']}_{agg['window_start']}"
        self.es.index(index='hashtag_trends', id=doc_id, body=agg)

    def flush(self):
        if self.buffer:
            helpers.bulk(self.es, self.buffer)
            logger.info(f'{len(self.buffer)} belge Elasticsearch\'e yazıldı.')
            self.buffer.clear()

def run_es_consumer(
    kafka_servers: str,
    result_topic:  str,
    aggreg_topic:  str
):
    """Kafka'dan Flink çıktısını okuyup Elasticsearch'e yazar."""
    tweet_consumer = KafkaConsumer(
        result_topic,
        bootstrap_servers=[kafka_servers],
        group_id='es_tweet_sink',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        max_poll_records=100
    )
    es_sink = ElasticsearchSink()

    logger.info('Elasticsearch Sink başlatıldı.')
    for msg in tweet_consumer:
        es_sink.index_tweet(msg.value)

if __name__ == '__main__':
    run_es_consumer('localhost:9092', 'sentiment_results', 'hashtag_aggregations')

# ================================================================
# Pipeline Performans İzleme ve Benchmarking
# ================================================================
import json, time, statistics
from kafka import KafkaConsumer
from collections import deque, defaultdict
from datetime import datetime

class PipelineMonitor:
    """
    Uçtan Uca Gecikme (End-to-End Latency) Ölçer.

    Gecikme = analyzed_at - ingestion_ts
    (Kafka'ya giriş anından Flink işleme bitimine kadar)
    """
    def __init__(self, window_size: int = 1000):
        self.latencies      = deque(maxlen=window_size)
        self.throughput_log = deque(maxlen=60)  # Son 60 saniye
        self.label_counts   = defaultdict(int)
        self.start_time     = time.time()
        self.total_messages = 0

    def record(self, tweet: dict):
        analyzed_at  = tweet.get('analyzed_at', time.time())
        ingestion_ts = tweet.get('ingestion_ts', analyzed_at)
        latency_ms   = (analyzed_at - ingestion_ts) * 1000

        if 0 < latency_ms < 60000:  # Makul aralık: 0-60sn
            self.latencies.append(latency_ms)

        label = tweet.get('final_label', 'UNKNOWN')
        self.label_counts[label] += 1
        self.total_messages += 1

    def report(self) -> dict:
        elapsed = time.time() - self.start_time
        if not self.latencies:
            return {}
        lat = list(self.latencies)
        return {
            'timestamp':         datetime.now().isoformat(),
            'total_messages':    self.total_messages,
            'throughput_msg_s':  round(self.total_messages / elapsed, 1),
            'latency_p50_ms':    round(statistics.median(lat), 1),
            'latency_p95_ms':    round(statistics.quantiles(lat, n=20)[18], 1),
            'latency_p99_ms':    round(statistics.quantiles(lat, n=100)[98], 1),
            'latency_max_ms':    round(max(lat), 1),
            'sentiment_dist':    dict(self.label_counts),
        }

def run_monitor(kafka_servers: str = 'localhost:9092',
               topic: str = 'sentiment_results'):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[kafka_servers],
        group_id='pipeline_monitor',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest'
    )
    monitor = PipelineMonitor()
    print(f'Pipeline Monitor başlatıldı. Topic: {topic}')

    last_report = time.time()
    for msg in consumer:
        monitor.record(msg.value)

        # Her 10 saniyede bir rapor yazdır
        if time.time() - last_report > 10:
            report = monitor.report()
            print(json.dumps(report, indent=2, ensure_ascii=False))
            last_report = time.time()

if __name__ == '__main__':
    run_monitor()
