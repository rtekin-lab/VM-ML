# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.2. Hadoop Ekosistemi ve MapReduce Mantığı › 12.2.3. Disk Darboğazı ve İteratif Algoritmaların Sorunu › Python Uygulaması: MapReduce'un Disk Darboğazını Simülasyonla Gösterme
# Kitap  : Kod 12.6 (Disk ve bellek erişiminin iteratif algoritma)
# Dosya : bolum12/12_02_03_python-uygulamasi-mapreduce-un-disk-darbogazini.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================
# ============================================================
# Disk vs RAM Gecikme Farkının İteratif Algoritmalara Etkisi
# Simülasyon: K-Means'in Hadoop vs Spark bağlamında süre tahmini
# ============================================================
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI olmayan ortamlar için
import matplotlib.pyplot as plt

# ---- GECIKME SABİTLERİ (nanosaniye cinsinden) ----
LATENCY_RAM_NS  = 100          # RAM: ~100 ns
LATENCY_HDD_NS  = 10_000_000  # HDD: ~10 ms = 10M ns
LATENCY_SSD_NS  = 100_000      # SSD: ~0.1 ms = 100K ns

# Bant genişliği (MB/s)
BW_RAM_MBS = 50_000    # DDR4: ~50 GB/s
BW_HDD_MBS = 200       # HDD:  ~200 MB/s
BW_SSD_MBS = 3_500     # NVMe: ~3.5 GB/s

def sure_hesapla(veri_mb, iterasyon, depolama='hdd'):
    """
    K-Means'in MapReduce (disk) vs Spark (RAM) süresini hesapla
    veri_mb   : Veri seti boyutu MB
    iterasyon : K-Means iterasyon sayısı
    """
    # Disk tabanlı hesap (MapReduce)
    bw = BW_HDD_MBS if depolama == 'hdd' else BW_SSD_MBS
    disk_transfer_sure = veri_mb / bw   # saniye
    islem_sure_iter    = 0.05 * veri_mb / 1024   # 50 ms/GB hesaplama

    # Her iterasyon: 1 okuma + 1 yazma + hesaplama
    hadoop_sure = (disk_transfer_sure * 2 + islem_sure_iter) * iterasyon

    # RAM tabanlı hesap (Spark)
    ram_transfer = veri_mb / BW_RAM_MBS
    ilk_okuma   = disk_transfer_sure   # İlk kez diskten yükle
    spark_sure  = ilk_okuma + (ram_transfer + islem_sure_iter) * iterasyon

    return hadoop_sure, spark_sure

# ---- ANALİZ: Farklı iterasyon sayılarında süre karşılaştırması ----
VERI_MB = 10_000   # 10 GB veri seti
iterasyonlar = list(range(1, 101))  # 1 - 100 iterasyon

hadoop_sureler = []
spark_sureler  = []

for it in iterasyonlar:
    h, s = sure_hesapla(VERI_MB, it, 'hdd')
    hadoop_sureler.append(h / 60)   # dakikaya çevir
    spark_sureler.append(s / 60)

# Sonuçları yazdır
print(f'=== 10 GB Veri, K-Means Süre Karşılaştırması ===')
print(f'{"İterasyon":<15} {"Hadoop (dk)":>12} {"Spark (dk)":>12} {"Hız Kazanımı":>14}')
print('-' * 55)
for it in [1, 5, 10, 20, 50, 100]:
    h_dk = hadoop_sureler[it-1]
    s_dk = spark_sureler[it-1]
    kazanim = h_dk / s_dk if s_dk > 0 else float('inf')
    print(f'{it:<15} {h_dk:>12.1f} {s_dk:>12.2f} {kazanim:>13.0f}×')

# ============================================================
# GERCEK OLCUM: ara sonucu diske yazmak ne kadara mal oluyor?
# ------------------------------------------------------------
# Yukaridaki hesap analitik bir MODELDIR. Asagida ayni iteratif
# hesap iki bicimde GERCEKTEN calistirilip suresi olculur:
#   (a) her iterasyonun ciktisi diske yazilip geri okunur (MapReduce)
#   (b) ara sonuc bellekte tutulur (Spark)
# Mutlak degerler donaniminiza gore degisir; onemli olan EGIMLER ORANI.
# ============================================================
import os, tempfile

def kmeans_adimi(X, merkezler):
    """Tek K-Means iterasyonu: atama + merkez guncelleme."""
    d = ((X[:, None, :] - merkezler[None, :, :]) ** 2).sum(axis=2)
    etiket = d.argmin(axis=1)
    return np.array([X[etiket == k].mean(axis=0) if (etiket == k).any()
                     else merkezler[k] for k in range(len(merkezler))])

def olc(X, k=4, n_iter=20, diske_yaz=False):
    rng = np.random.default_rng(0)
    merkezler = X[rng.choice(len(X), k, replace=False)]
    gecici = os.path.join(tempfile.gettempdir(), "vmml_ara_sonuc.npy")
    sureler, t0 = [], time.perf_counter()
    for _ in range(n_iter):
        merkezler = kmeans_adimi(X, merkezler)
        if diske_yaz:                      # MapReduce: ara sonuc diske yazilir
            with open(gecici, "wb") as f:
                np.save(f, X)
                f.flush()
                os.fsync(f.fileno())       # isletim sistemi onbellegini atla:
                                           # olculen sey gercek disk turu olsun
            X = np.load(gecici)
        sureler.append(time.perf_counter() - t0)
    if os.path.exists(gecici):
        os.remove(gecici)
    return sureler

np.random.seed(0)
# Veri, isletim sistemi sayfa onbellegine tam sigmayacak kadar buyuk secilir;
# aksi halde "diske yazma" gercekte diske hic gitmez ve fark kaybolur.
X_olc = np.random.randn(150_000, 24).astype(np.float32)
N_IT = 20
s_disk = olc(X_olc.copy(), n_iter=N_IT, diske_yaz=True)
s_ram  = olc(X_olc.copy(), n_iter=N_IT, diske_yaz=False)
oran = s_disk[-1] / s_ram[-1]
print(f"\n=== Gercek olcum ({N_IT} iterasyon, {X_olc.nbytes/1e6:.0f} MB) ===")
print(f"Diske yazarak : {s_disk[-1]:.2f} s")
print(f"Bellekte      : {s_ram[-1]:.2f} s")
print(f"Fark          : {oran:.1f}x")

# ---- GRAFIK ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.plot(range(1, N_IT + 1), s_disk, "r-o", markersize=4,
         label=f"Ara sonuc diske ({s_disk[-1]:.2f} s)")
ax1.plot(range(1, N_IT + 1), s_ram, "b-o", markersize=4,
         label=f"Ara sonuc bellekte ({s_ram[-1]:.2f} s)")
ax1.set_xlabel("Iterasyon"); ax1.set_ylabel("Kumulatif sure (s)")
ax1.set_title(f"Olculen: ayni K-Means, iki veri yolu\n{X_olc.nbytes/1e6:.0f} MB, fark {oran:.1f}x")
ax1.legend(fontsize=9); ax1.grid(alpha=0.3)

ax2.plot(iterasyonlar, hadoop_sureler, "r--", lw=1.6, label="MapReduce (HDD)")
ax2.plot(iterasyonlar, spark_sureler, "b--", lw=1.6, label="Spark (RAM)")
ax2.set_xlabel("Iterasyon Sayisi (K-Means)"); ax2.set_ylabel("Sure (dakika)")
ax2.set_title("Analitik model: 10 GB veri\n(olcum degil, gecikme sabitlerinden turetilmistir)")
ax2.legend(fontsize=9); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
