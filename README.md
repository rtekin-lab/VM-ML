# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ — Kod Deposu

*Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere*

Kitaptaki tüm kod örneklerinin çalışır hâli. Her dosya bağımsız olarak çalıştırılabilir; kitapta önceki bloklarda kalan `import` satırları dosya başına eklenmiştir.

## Kurulum

```bash
git clone https://github.com/rtekin-lab/VM-ML.git
cd VM-ML
pip install -r kod/requirements.txt
```

Ya da bölüm bazında: `pip install -r kod/bolum06/requirements.txt`

## Bölümler

| Bölüm | Konu | Dosya | Kod satırı | Colab |
|---|---|---|---|---|
| 1 | [Python Ortamının Hazırlanması ve Temel Python Konuları](bolum01/README.md) | 89 | 2134 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum01.ipynb) |
| 2 | [VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER](bolum02/README.md) | 20 | 703 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum02.ipynb) |
| 3 | [Veri Ön İşleme ve Temizleme Teknikleri](bolum03/README.md) | 38 | 1037 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum03.ipynb) |
| 4 | [Veri Görselleştirme Araçları](bolum04/README.md) | 35 | 1892 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum04.ipynb) |
| 5 | [MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ](bolum05/README.md) | 6 | 427 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum05.ipynb) |
| 6 | [Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine](bolum06/README.md) | 7 | 371 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum06.ipynb) |
| 7 | [GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME](bolum07/README.md) | 7 | 445 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum07.ipynb) |
| 8 | [BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ](bolum08/README.md) | 7 | 332 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum08.ipynb) |
| 9 | [Metin Madenciliği ve Doğal Dil İşleme (NLP)](bolum09/README.md) | 12 | 648 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum09.ipynb) |
| 10 | [YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS)](bolum10/README.md) | 17 | 838 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 11 | [DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON](bolum11/README.md) | 11 | 879 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum11.ipynb) |
| 12 | [BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ](bolum12/README.md) | 13 | 879 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum12.ipynb) |
| 13 | [VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK](bolum13/README.md) | 7 | 1542 | [▶ Aç](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum13.ipynb) |

**Toplam: 269 dosya, 12127 kod satırı**

## Dosya adlandırma

```
bolum03/03_01_07_03_knn-imputation.py
       │  │  │  │  └─ alt bölüm başlığından türetilmiş ad
       │  │  │  └──── kitaptaki alt bölüm no (3.1.7.3)
       └──┴──┴─────── bölüm ve kesim numaraları
```

## Dosya türleri

| Uzantı | Anlamı |
|---|---|
| `.py` | Python betiği |
| `.sh` | Kabuk / terminal komutları |
| `.ipy` | IPython / Colab hücresi (magic komut içerir) |
| `.sql` | SQL |
| `.yml` | YAML yapılandırma |
| `.txt` | Sözde kod / algoritma |

## Depoyu ilk kez yükleme

```bash
cd kod
git init
git add .
git commit -m "Kitabın kod örnekleri: 269 betik, 13 Colab defteri"
git branch -M main
git remote add origin https://github.com/rtekin-lab/VM-ML.git
git push -u origin main
```

Colab bağlantılarının çalışması için depo **public** olmalı ve dosyalar
`kod/` klasörü altında, ana dal (`main`) üzerinde bulunmalıdır.

## Araçlar

`arac/` klasöründe, kitaptaki şekilleri kod dosyalarından üreten betikler
ve kullanım kılavuzu bulunur.

## Not

Kitaptaki kod blokları öğretici amaçla kısaltılmıştır; tam ve çalışır sürüm her zaman bu depodadır. Kitapta her kod bloğunun altında ilgili dosyanın adı verilmiştir.
