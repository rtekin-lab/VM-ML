# Şekil Üretim Araçları

Kitaptaki kod örneklerini çalıştırıp ürettikleri grafikleri PNG olarak kaydeden ve
bunları Word bölümlerine "Şekil N.k" açıklamalarıyla yerleştiren iki betik.

25 şekil, sınırlı bir ortamda (yalnızca numpy / pandas / matplotlib / seaborn /
scipy / scikit-learn kurulu, internet kapalı) zaten üretildi. Kalan ~155 şekil için
aşağıdaki adımlar izlenmelidir.

## Neden kalan şekiller üretilemedi?

| Neden | Dosya sayısı |
|---|---|
| Kurulu olmayan kütüphane (tensorflow, plotly, statsmodels, pyspark, nltk, gensim…) | 74 |
| İnternet gerektiren veri seti indirmesi (`seaborn.load_dataset`, `fetch_openml`, HTTP 403) | 16 |
| Dosyada zaten grafik yok | 71 |
| Şekil üretildi | 22 (25 şekil) |

## Adımlar

### 1. Ortamı kur

```bash
conda create -n vmml-sekil python=3.11 -y
conda activate vmml-sekil
pip install -r kod/arac/requirements-sekil.txt
pip install python-docx
```

`pyspark` ve `apache-flink` gerektiren dosyalar grafik üretmez; kurmanıza gerek yok.

### 2. NLTK / veri seti önbelleklerini indir

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('vader_lexicon')"
```

seaborn örnek veri setleri ilk çalıştırmada otomatik iner (internet gerekir).

### 3. Şekilleri üret

Önce ne olacağını görün (hiçbir şey değiştirmez):

```bash
python kod/arac/sekil_uret.py --liste
```

Bu komut hangi dosyanın çalıştırılacağını, hangisinin hangi kütüphane eksik olduğu
için atlanacağını satır satır yazar. Eksik listesi kabul edilebilir olunca çalıştırın:

```bash
python kod/arac/sekil_uret.py                 # tüm bölümler
python kod/arac/sekil_uret.py --bolum 4       # yalnızca 4. bölüm (önerilir)
```

- Yolları kendisi bulur (`kod/arac/` konumuna göre). Gerekirse elle verilebilir:
  `--kod ./kod --cikti ./sekiller`
- Her `.py` dosyasını ayrı bir süreçte, `matplotlib Agg` arka ucuyla çalıştırır.
- `plt.show()` çağrısını yakalayıp açık figürleri kaydeder; `input()` çağrılarını susturur.
- Dosya başına 90 sn zaman aşımı (`--zaman-asimi` ile değiştirilir).
- Çıktı: `sekiller/bolumNN__dosya-adi__01.png`
- Rapor: `sekil_sonuc.json`

Eksik kütüphaneler **otomatik** tespit edilir; elle liste düzenlemeniz gerekmez.

### 4. Üretilen şekilleri gözden geçir

Otomatik üretilen her şekil kitaba girmeye uygun olmayabilir. `sekiller/` klasörünü
açıp okunaksız, boş veya tekrarlı olanları **silin**. 5. adım yalnızca klasörde kalan
dosyaları yerleştirir.

### 5. Kitaba yerleştir

```bash
pip install python-docx
python kod/arac/sekil_yerlestir.py --bolumler ./bolumler --onizleme   # önce dene
python kod/arac/sekil_yerlestir.py --bolumler ./bolumler              # sonra uygula
```

- `.docx` içindeki `📄 Tam kod: kod/bolumNN/…` satırını bulup şekli tam onun
  altına ekler; açıklamayı `Şekil N.k: <en yakın başlık>` biçiminde yazar.
- Her dosyanın yanına `*.docx.yedek` bırakır.
- **Çift ekleme sorunu yok:** betik, daha önce yerleştirilmiş şekilleri ve
  açıklamalarını silip numaralandırmayı baştan yapar. Bu davranışı kapatmak için
  `--koru` kullanın (o zaman numaralar çakışabilir).

`--bolumler` yolunu vermezseniz betik `./bolumler` klasörünü arar.

## Öneri

Bu işi bölüm bölüm yapın: önce Bölüm 4 (Matplotlib/Seaborn/Plotly — en çok şekil
buradan çıkacak), sonra Bölüm 10–11 (TensorFlow eğitim eğrileri), sonra Bölüm 6 ve 9.
Her bölümden sonra çıktıyı gözle kontrol edin.

```bash
python kod/arac/sekil_uret.py --bolum 4
#   sekiller/ klasörünü aç, kötüleri sil
python kod/arac/sekil_yerlestir.py --bolumler ./bolumler
```

## Sorun giderme

| Belirti | Neden / çözüm |
|---|---|
| `{}` ve `üretilen şekil: 0` | Eski sürüm hatası. Bu sürüm yolu bulamazsa açık hata verir. |
| `HATA: … altında .py dosyası yok` | Yanlış klasördesiniz. `--kod ./kod` ile yolu verin. |
| Çok dosya "ATLANIR" diyor | `pip install -r kod/arac/requirements-sekil.txt` |
| `HTTP Error 403` / indirme hatası | İnternet kapalı ya da veri kaynağı erişimi engelliyor. |
| Şekiller iki kez eklendi | `--koru` kullanmayın; betik varsayılan olarak eskileri temizler. |
| `UnicodeEncodeError: 'charmap'` | Windows konsolu cp1254. Bu sürümde alt süreç UTF-8'e zorlanır; sorun çıkarsa `set PYTHONUTF8=1`. |
| `FileNotFoundError: /tmp/...` | Sabit POSIX yolu. Bu sürümde `tempfile.gettempdir()` kullanılıyor. |
| `zaman aşımı` (TensorFlow dosyaları) | `--zaman-asimi 300` verin; TF modelleri 90 sn'ye sığmıyor. |
| `pkg_resources` eksik | Python 3.12+ ile gelmiyor; kod `importlib.metadata` kullanacak şekilde güncellendi. |
| Şekil eski hâlinde çıkıyor | `python kod/arac/sekil_uret.py --denetle` çalıştırın. "ESKI" satırı varsa `kod/` klasörünü **silip** zip'i yeniden açın (üzerine yazmak Dropbox/Drive senkronunda yetmeyebilir). |

## Güncellik denetimi

```bash
python kod/arac/sekil_uret.py --denetle
```

Bilinen düzeltmelerin dosyalarda bulunup bulunmadığını satır satır raporlar.
Şekil üretmeden önce bunu çalıştırmak, eski dosyalarla uğraşmayı önler.
