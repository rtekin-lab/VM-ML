# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.5. Uçtan Uca Vaka Çalışması (Case Study): › 13.5.2. Veri Üretimi: Tweepy ile Canlı Twitter Akışı ve Kafka'ya İletim
# Kitap  : Kod 13.7 (Kafka üreticisiyle tweet akışı benzetimi)
# Dosya : bolum13/13_05_02_veri-uretimi-tweepy-ile-canli-twitter-akisi-ve-k.py
# Gerekli: pip install kafka-python tweepy
# ==========================================================================
# ================================================================
# Twitter Filtered Stream + Kafka Producer
# pip install tweepy kafka-python
# ================================================================
import tweepy
import json
import re
import time
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ---- Tweet Temizleme Yardımcı Fonksiyon ----
def clean_tweet(text: str) -> str:
    """
    NLP modellerinin daha iyi sonuç vermesi için tweet metnini temizler.
    Sıralı dönüşümler:
    1. URL'ler kaldırılır
    2. @mention'lar kaldırılır
    3. RT (retweet) öneki kaldırılır
    4. Çift boşluklar tekleştirilir
    5. Baştaki/sondaki boşluklar temizlenir
    """
    text = re.sub(r'http\S+|www\.\S+', '', text)       # URL'ler\ntext = re.sub(r'@\w+', '', text)                    # Mention'lar
    text = re.sub(r'^RT\s?:', '', text)                 # Retweet öneki
    text = re.sub(r'#', '', text)                        # Hashtag sembolü (#AI → AI)
    text = re.sub(r'\s+', ' ', text)                    # Çift boşluklar
    return text.strip()

# ---- Kafka Producer Fabrikası ----
def create_producer(bootstrap_servers: list) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all',
        retries=5,
        linger_ms=10,
        compression_type='lz4'
    )

# ---- Tweepy StreamingClient Alt Sınıfı ----
class TweetStreamToKafka(tweepy.StreamingClient):
    """
    Tweepy StreamingClient'ı genişleterek gelen her tweet'i
    Kafka'ya iletir.
    """
    TOPIC_NAME     = 'tweet_stream'
    TARGET_LANGS   = {'en', 'tr'}  # Hangi dilleri işleyeceğiz

    def __init__(self, bearer_token: str, kafka_servers: list, **kwargs):
        super().__init__(bearer_token, **kwargs)
        self.producer    = create_producer(kafka_servers)
        self.tweet_count = 0
        self.error_count = 0

    def on_tweet(self, tweet):
        """Her yeni tweet geldiğinde otomatik olarak çağrılır."""
        try:
            # Dil filtresi: sadece hedef dilleri işle
            lang = getattr(tweet, 'lang', 'und')
            if lang not in self.TARGET_LANGS:
                return

            # Hashtag listesi çıkar
            hashtags = []
            if hasattr(tweet, 'entities') and tweet.entities:
                ht_list = tweet.entities.get('hashtags', [])
                hashtags = [ht['tag'].lower() for ht in ht_list]

            # Metrik bilgileri
            metrics = {}
            if hasattr(tweet, 'public_metrics') and tweet.public_metrics:
                metrics = tweet.public_metrics

            # Kafka'ya gönderilecek payload oluştur
            payload = {
                'tweet_id':      str(tweet.id),
                'text':          tweet.text,
                'clean_text':    clean_tweet(tweet.text),
                'lang':          lang,
                'author_id':     str(tweet.author_id) if tweet.author_id else None,
                'hashtags':      hashtags,
                'retweet_count': metrics.get('retweet_count', 0),
                'like_count':    metrics.get('like_count', 0),
                # Event Time: tweet'in gerçek oluşturulma zamanı
                'created_at':    tweet.created_at.isoformat() if tweet.created_at else None,
                # Ingestion Time: Kafka'ya girdiği an
                'ingestion_ts':  time.time()
            }

            # Partition key: dil kodu (aynı dil → aynı partition → sıra garantisi)
            self.producer.send(
                self.TOPIC_NAME,
                key=lang,
                value=payload
            )
            self.tweet_count += 1

            if self.tweet_count % 100 == 0:
                logger.info(f"Kafka'ya gönderilen tweet: {self.tweet_count}")

        except Exception as e:
            self.error_count += 1
            logger.error(f'Tweet işleme hatası: {e}')

    def on_error(self, status_code):
        logger.error(f'Twitter API Hatası: {status_code}')
        if status_code == 429:  # Rate limit
            logger.warning('Rate limit aşıldı. 60 saniye bekleniyor...')
            time.sleep(60)
        return True  # True: bağlantıyı koru

    def on_disconnect(self):
        logger.warning('Twitter bağlantısı kesildi. Yeniden bağlanılıyor...')
        self.producer.flush()

# ---- Filtreleme Kuralları Yönetimi ----
def setup_stream_rules(client: TweetStreamToKafka, keywords: list):
    """
    Mevcut kuralları temizle ve yeni kurallar ekle.
    Twitter API v2 kural dili örnekleri:
    - 'python lang:en -is:retweet'  → İngilizce python tweet'leri, RT hariç
    - '#AI OR #MachineLearning'      → Bu hashtag'lerden biri olan tweet'ler
    - 'yapay zeka lang:tr'           → Türkçe yapay zeka tweet'leri
    """
    # Mevcut kuralları sil
    existing = client.get_rules().data
    if existing:
        rule_ids = [rule.id for rule in existing]
        client.delete_rules(rule_ids)
        logger.info(f'{len(rule_ids)} eski kural silindi.')

    # Yeni kurallar ekle
    new_rules = []
    for kw in keywords:
        rule_text = f'{kw} -is:retweet lang:en OR lang:tr'
        new_rules.append(tweepy.StreamRule(rule_text))
    client.add_rules(new_rules)
    logger.info(f'{len(new_rules)} yeni kural eklendi: {keywords}')

# ---- Ana Çalıştırıcı ----
def run_twitter_stream(
    bearer_token: str,
    kafka_servers: list,
    keywords: list
):
    stream = TweetStreamToKafka(
        bearer_token=bearer_token,
        kafka_servers=kafka_servers,
        wait_on_rate_limit=True  # Rate limit'e çarparsa otomatik bekle
    )
    setup_stream_rules(stream, keywords)

    logger.info(f'Twitter akışı başlatılıyor. Anahtar kelimeler: {keywords}')
    stream.filter(
        tweet_fields=['created_at', 'lang', 'author_id', 'public_metrics'],
        expansions=['entities.mentions.username'],
        media_fields=['url']
    )

# Gerçek kullanım:
# run_twitter_stream(
#     bearer_token='YOUR_BEARER_TOKEN',
#     kafka_servers=['localhost:9092'],
#     keywords=['yapay zeka', 'artificial intelligence', '#AI']
# )

# ================================================================
# Gerçekçi Tweet Simülatörü — Production-grade test ortamı
# ================================================================
import json, time, random, uuid, re
from datetime import datetime, timezone
from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TweetSimulator')

# Gerçekçi tweet şablonları (çeşitli duygu tonları)
TWEET_TEMPLATES = {
    'positive': [
        '{topic} gerçekten harika! Bu teknolojiyi çok seviyorum. #innovation',
        'Bugün {topic} hakkında muhteşem bir şey öğrendim. Geleceğe umutla bakıyorum!',
        '{topic} ile yapılan bu proje inanılmaz sonuçlar veriyor. Tebrikler ekibe!',
        'Finally understood {topic} and it is absolutely amazing! #tech #AI',
        '{topic} is revolutionizing everything. Cant wait to see whats next!'
    ],
    'negative': [
        '{topic} hâlâ pek çok sorunu çözemiyor. Hayal kırıklığı büyük.',
        'Bu {topic} ürünü tam bir hayal kırıklığı. Param çöpe gitti.',
        '{topic} ile ilgili bu gelişme endişe verici. Kimse önlem almıyor.',
        'Disappointed with {topic}. Expected much more. #fail',
        '{topic} is overhyped and underdelivering. Not impressed at all.'
    ],
    'neutral': [
        '{topic} hakkında yeni bir rapor yayınlandı. İnceliyorum.',
        'Bugün {topic} konferansına katıldım. Notlar hazırlıyorum.',
        '{topic} trends are changing rapidly. Interesting to observe.',
        'New study about {topic} published today. Worth reading.',
        '{topic} market update: mixed signals from analysts.'
    ]
}

TOPICS = ['yapay zeka', 'artificial intelligence', 'machine learning',
          'deep learning', 'ChatGPT', 'data science', 'Python', 'Flink']

HASHTAG_POOL = {
    'tech': ['AI', 'MachineLearning', 'DataScience', 'DeepLearning', 'Python'],
    'business': ['Innovation', 'Tech', 'Startup', 'Digital', 'Future'],
    'community': ['OpenSource', 'Developer', 'Programming', 'TechTwitter']
}

LANGUAGES = ['en', 'en', 'en', 'tr', 'tr']  # İngilizce ağırlıklı

def generate_mock_tweet(topic: str = None) -> dict:
    """
    Gerçekçi duygu dağılımı simüle eden tweet üretir:
    Pozitif: %45, Negatif: %30, Nötr: %25
    (Gerçek Twitter duygu dağılımına yakın değerler)
    """
    if topic is None:
        topic = random.choice(TOPICS)

    # Gerçekçi duygu dağılımı
    rand = random.random()
    if rand < 0.45:
        sentiment = 'positive'
    elif rand < 0.75:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    lang = random.choice(LANGUAGES)

    # Tweet metni oluştur
    template = random.choice(TWEET_TEMPLATES[sentiment])
    text = template.format(topic=topic)

    # Hashtag'ler ekle
    category = random.choice(list(HASHTAG_POOL.keys()))
    hashtags = random.sample(HASHTAG_POOL[category], k=random.randint(1, 3))

    # Gerçekçi engagement metrikleri (uzun kuyruklu dağılım)
    follower_weight = random.paretovariate(1.5)
    retweet_count   = int(random.expovariate(0.1) * follower_weight)
    like_count      = int(retweet_count * random.uniform(2, 10))

    return {
        'tweet_id':      str(uuid.uuid4()),
        'text':          text + ' ' + ' '.join(f'#{h}' for h in hashtags),
        'clean_text':    re.sub(r'#\w+', '', text).strip(),
        'lang':          lang,
        'author_id':     f'user_{random.randint(10000, 9999999)}',
        'hashtags':      hashtags,
        'retweet_count': retweet_count,
        'like_count':    like_count,
        'created_at':    datetime.now(timezone.utc).isoformat(),
        'ingestion_ts':  time.time(),
        # Ground truth label (simülatör bilir, gerçekte yoktur)
        '_sim_sentiment': sentiment
    }

def run_mock_producer(
    kafka_servers: list,
    topic_name: str = 'tweet_stream',
    tweets_per_second: float = 50.0,
    burst_mode: bool = False
):
    """
    Ayarlanabilir hızda tweet akışı simüle eder.
    burst_mode=True ile zirve trafik simülasyonu yapılabilir.
    """
    producer = KafkaProducer(
        bootstrap_servers=kafka_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8'),
        compression_type='lz4',
        linger_ms=5
    )

    sleep_interval = 1.0 / tweets_per_second
    sent   = 0
    topic  = random.choice(TOPICS)

    logger.info(f'Mock Producer: {tweets_per_second} tweet/sn hızında başlatıldı.')

    try:
        while True:
            # Burst modu: her 60sn'de 10sn boyunca 10x trafik
            if burst_mode and sent % 3000 == 2999:
                logger.info('BURST MODE başlıyor — 10 saniye yüksek trafik!')
                for _ in range(int(tweets_per_second * 10 * 10)):  # 10x * 10sn
                    tweet = generate_mock_tweet()
                    producer.send(topic_name, key=tweet['lang'], value=tweet)
                logger.info('BURST MODE bitti.')
                producer.flush()

            tweet = generate_mock_tweet(topic=topic)
            producer.send(topic_name, key=tweet['lang'], value=tweet)
            sent += 1

            # Her 1000 tweet'te topic değiştir (trending topic simülasyonu)
            if sent % 1000 == 0:
                topic = random.choice(TOPICS)
                logger.info(f'Gönderilen: {sent} | Güncel topic: {topic}')
                producer.flush()

            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        logger.info(f'Simülatör durduruldu. Toplam: {sent} tweet.')
    finally:
        producer.flush()
        producer.close()

if __name__ == '__main__':
    run_mock_producer(
        kafka_servers=['localhost:9092'],
        tweets_per_second=50,  # Saniyede 50 tweet
        burst_mode=True        # Zirve trafik testi
    )
