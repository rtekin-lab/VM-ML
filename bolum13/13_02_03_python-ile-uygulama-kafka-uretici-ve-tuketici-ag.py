# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.2. Apache Kafka: Dağıtık Mesajlaşma ve Veri Akışı Platformu › 13.2.3. Python ile Uygulama: Kafka Üretici ve Tüketici Ağı
# Dosya : bolum13/13_02_03_python-ile-uygulama-kafka-uretici-ve-tuketici-ag.py
# Gerekli: pip install kafka-python
# ==========================================================================
# ============================================================
# KAFKA PRODUCER (ÜRETİCİ) — Gelişmiş Clickstream Simülasyonu
# pip install kafka-python
# ============================================================
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import random
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---- Kafka Producer Konfigürasyonu ----
def create_producer(bootstrap_servers: list) -> KafkaProducer:
    """
    Kafka Producer oluşturur. Parametre açıklamaları:
    - value_serializer: Python dict'i JSON byte'ına çevirir (serileştirme)
    - key_serializer:   Partition anahtarını UTF-8 byte'ına çevirir
    - acks='all':       Tüm in-sync replica'lar yazıyı onaylayana kadar bekle (güvenilir)
    - retries:          Başarısız yazımda 3 kez yeniden dene
    - compression_type: lz4 sıkıştırma — yüksek hacimde ağ ve depolama tasarrufu
    - linger_ms:        Mesajları 5ms biriktir, sonra toplu gönder (throughput artışı)
    """
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all',
        retries=3,
        compression_type='lz4',
        linger_ms=5,
        batch_size=65536  # 64KB — toplu gönderim için tampon boyutu
    )

def on_send_success(record_metadata):
    logger.info(f"Mesaj gönderildi | Topic: {record_metadata.topic} | "
                f"Partition: {record_metadata.partition} | Offset: {record_metadata.offset}")

def on_send_error(excp):
    logger.error(f"Mesaj gönderim hatası: {excp}")

# ---- Ana Üretici Döngüsü ----
def run_producer():
    producer = create_producer(['localhost:9092'])
    TOPIC = 'user_clickstream'
    PRODUCTS = ['laptop', 'phone', 'headphones', 'tablet', 'smartwatch', 'camera']
    CATEGORIES = ['elektronik', 'giyim', 'ev-bahce', 'spor', 'kitap']
    ACTIONS = ['view_product', 'add_to_cart', 'remove_from_cart', 'checkout', 'purchase', 'search']

    logger.info(f"Producer başlatıldı. Topic: {TOPIC}")
    sent_count = 0

    try:
        while True:
            user_id = f"user_{random.randint(1000, 9999)}"

            # Her mesaj için partition key olarak user_id kullanılır.
            # Aynı kullanıcının tüm olayları aynı partition'a gider => sıra garantisi
            event = {
                'event_id':    str(uuid.uuid4()),
                'user_id':     user_id,
                'session_id':  f"session_{random.randint(100, 999)}",
                'action':      random.choice(ACTIONS),
                'product':     random.choice(PRODUCTS),
                'category':    random.choice(CATEGORIES),
                'price':       round(random.uniform(9.99, 4999.99), 2),
                'quantity':    random.randint(1, 5),
                'device':      random.choice(['mobile', 'desktop', 'tablet']),
                'country':     random.choice(['TR', 'DE', 'US', 'GB', 'FR']),
                'timestamp':   time.time(),
                'event_time':  time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }

            # Asenkron gönderim (callback ile) — throughput için kritik
            future = producer.send(
                TOPIC,
                key=user_id,    # Aynı kullanıcı => aynı partition
                value=event
            )
            future.add_callback(on_send_success).add_errback(on_send_error)

            sent_count += 1
            if sent_count % 100 == 0:
                producer.flush()  # Arabellekteki mesajları zorla gönder
                logger.info(f"Toplam gönderilen: {sent_count} mesaj")

            time.sleep(0.1)  # 10 mesaj/saniye hızında üretim

    except KeyboardInterrupt:
        logger.info("Producer durduruluyor...")
    finally:
        producer.flush()
        producer.close()
        logger.info(f"Producer kapatıldı. Toplam gönderilen: {sent_count} mesaj")

if __name__ == '__main__':
    run_producer()

# ============================================================
# KAFKA CONSUMER (TÜKETİCİ) — Gerçek Zamanlı Analitik Motoru
# ============================================================
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
from collections import defaultdict, deque
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---- Kayan Pencere Tabanlı İstatistik Takipçisi ----
class SlidingWindowTracker:
    """
    Her kullanıcı için son N olaydaki harcama toplamını
    O(1) bellek ve O(1) güncelleme karmaşıklığıyla takip eder.
    Bu yapı, akan veri üzerinde Konsept Kaymasına duyarlı anomali tespiti için temeldir.
    """
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.user_events = defaultdict(lambda: deque(maxlen=window_size))
        self.user_totals = defaultdict(float)

    def add_event(self, user_id: str, price: float, action: str) -> dict:
        window = self.user_events[user_id]

        # Pencere dolduysa en eski değeri toplamdan çıkar
        if len(window) == self.window_size:
            old_price, old_action = window[0]
            if old_action in ('purchase', 'checkout'):
                self.user_totals[user_id] -= old_price

        window.append((price, action))
        if action in ('purchase', 'checkout'):
            self.user_totals[user_id] += price

        return {
            'user_id':         user_id,
            'window_total':    round(self.user_totals[user_id], 2),
            'event_count':     len(window),
            'avg_price':       round(self.user_totals[user_id] / max(len(window), 1), 2)
        }

# ---- Kafka Consumer Konfigürasyonu ----
def create_consumer(topic: str, group_id: str, bootstrap_servers: list) -> KafkaConsumer:
    """
    Consumer parametreleri:
    - auto_offset_reset='latest':  Yalnızca bu consumer başladıktan sonra gelen
                                    mesajları işle (canlı akış modu)
    - enable_auto_commit=False:    Offset'i manuel yönetiyoruz (exactly-once için)
    - max_poll_records=100:        Tek poll çağrısında en fazla 100 mesaj al
    - session_timeout_ms=30000:    Consumer 30sn cevap vermezse ölü kabul edilir
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='latest',
        enable_auto_commit=False,  # Manuel commit — exactly-once için
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: x.decode('utf-8') if x else None,
        max_poll_records=100,
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000
    )

# ---- Anomali Tespit Kuralları ----
ANOMALY_RULES = {
    'yuksek_degerli_islem':   lambda e: e['action'] == 'purchase' and e['price'] > 2000,
    'hizli_sepet_dolumu':     lambda e: e['action'] == 'add_to_cart' and e['quantity'] > 4,
    'farkli_ulke_aniden':     lambda e: e.get('country') not in ['TR', 'DE']
}

def check_anomalies(event: dict, tracker_stats: dict) -> list:
    anomalies = []
    for rule_name, rule_fn in ANOMALY_RULES.items():
        try:
            if rule_fn(event):
                anomalies.append(rule_name)
        except Exception:
            pass

    # Pencere toplamına dayalı ek kural
    if tracker_stats['window_total'] > 5000:
        anomalies.append('pencere_harcama_limiti_asimi')

    return anomalies

# ---- Ana Tüketici Döngüsü ----
def run_consumer():
    consumer = create_consumer('user_clickstream', 'ml_analytics_group', ['localhost:9092'])
    tracker = SlidingWindowTracker(window_size=10)
    processed = 0

    logger.info("Consumer başlatıldı. Mesajlar dinleniyor...")

    try:
        for message in consumer:
            event = message.value
            user_id = message.key

            # 1. Kayan Pencere İstatistiklerini Güncelle
            stats = tracker.add_event(user_id, event['price'], event['action'])

            # 2. Anomali Tespiti
            anomalies = check_anomalies(event, stats)

            if anomalies:
                logger.warning(
                    f"ANOMALI TESPIT | Kullanıcı: {user_id} | "
                    f"Kurallar: {anomalies} | Pencere Toplam: {stats['window_total']} TL"
                )
                # Gerçek sistemde: fraud alert göndermek, hesabı askıya almak vb.

            # 3. Offset'i Manuel Commit Et (exactly-once için)
            # Sadece başarılı işlemden sonra commit yapılır
            consumer.commit({
                message.topic_partition: message.offset + 1
            } if hasattr(message, 'topic_partition') else None)
            # Basit versiyon:
            consumer.commit()

            processed += 1
            if processed % 1000 == 0:
                logger.info(f"İşlenen toplam mesaj: {processed}")

    except KeyboardInterrupt:
        logger.info("Consumer durduruluyor...")
    finally:
        consumer.close()

if __name__ == '__main__':
    run_consumer()

# ============================================================
# KAFKA ADMIN — Topic Oluşturma ve Yapılandırma
# ============================================================
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

def create_kafka_topics(bootstrap_servers: list, topics_config: list):
    """
    topics_config: [{'name': str, 'partitions': int, 'replication_factor': int, 'config': dict}]
    """
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='admin-client')

    new_topics = [
        NewTopic(
            name=t['name'],
            num_partitions=t['partitions'],
            replication_factor=t['replication_factor'],
            topic_configs=t.get('config', {})
        )
        for t in topics_config
    ]

    try:
        result = admin.create_topics(new_topics=new_topics, validate_only=False)
        for topic, error in result.topic_errors:
            if error is None or error == 0:
                print(f"Topic '{topic}' başarıyla oluşturuldu.")
            else:
                print(f"Topic '{topic}' oluşturma hatası: {error}")
    except TopicAlreadyExistsError:
        print("Topic zaten mevcut.")
    finally:
        admin.close()

# Kullanım Örneği:
create_kafka_topics(
    bootstrap_servers=['localhost:9092'],
    topics_config=[
        {
            'name': 'user_clickstream',
            'partitions': 12,            # 12 paralel okuma kapasitesi
            'replication_factor': 3,     # 3 kopya — 2 broker arızasına dayanıklı
            'config': {
                'retention.ms':      str(7 * 24 * 60 * 60 * 1000),  # 7 gün saklama
                'cleanup.policy':    'delete',   # Retention süresi dolunca sil
                'compression.type':  'lz4',      # Depolama sıkıştırması
                'min.insync.replicas': '2'       # En az 2 replica sync olmalı
            }
        },
        {
            'name': 'fraud_alerts',
            'partitions': 3,
            'replication_factor': 3,
            'config': {
                'retention.ms':    str(30 * 24 * 60 * 60 * 1000),  # 30 gün saklama
                'cleanup.policy':  'compact,delete'  # Compaction + retention
            }
        }
    ]
)
