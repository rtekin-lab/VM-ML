# Bölüm 10 — Kod Dosyaları

**BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS)**

17 dosya · 838 kod satırı

```bash
pip install -r requirements.txt
```

| # | Dosya | Kitap listesi | Kitaptaki yeri | Tür | Satır | Colab |
|---|---|---|---|---|---|---|
| 1 | `10_01_02_python-uygulamasi-mcculloch-pitts-noronu.py` | — | 10.1. Biyolojik Nöronlardan Yapay Ağlara Geçiş → Python Uygulaması: McCulloch-Pitts Nöronu | Python betiği | 64 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 2 | `10_02_01_python-uygulamasi-perceptron-sifirdan-kodlama.py` | Kod 10.1 | 10.2. Perceptron (Yapay Nöron) ve Doğrusal Sınıflandırma → Python Uygulaması: Perceptron Sıfırdan Kodlama | Python betiği | 105 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 3 | `10_02_02_cozum-iki-katmanli-ag-ile-xor-u-cozme.py` | — | 10.2. Perceptron (Yapay Nöron) ve Doğrusal Sınıflandırma → Çözüm: İki Katmanlı Ağ ile XOR'u Çözme | Python betiği | 62 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 4 | `10_03_02_python-keras-kodu-ile-ileri-yayilim-izleme.py` | Kod 10.2 | 10.3. Çok Katmanlı Algılayıcılar (Multi-Layer Perceptrons – MLP) → Python / Keras Kodu ile İleri Yayılım İzleme | Python betiği | 29 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 5 | `10_04_02_aktivasyon-fonksiyonlarinin-python-ile-gorselles.py` | Kod 10.3 | 10.4. Aktivasyon Fonksiyonları: Ağa Doğrusal Olmayanlık Kazandırma → Aktivasyon Fonksiyonlarının Python ile Görselleştirilmesi ve Karşılaştırılması | Python betiği | 67 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 6 | `10_04_kapsamli-uygulama-mlp-mimarisi-ve-aktivasyon-fon.py` | Kod 10.4 | 10.4. Aktivasyon Fonksiyonları: Ağa Doğrusal Olmayanlık Kazandırma → Kapsamlı Uygulama: MLP Mimarisi ve Aktivasyon Fonksiyonu Optimizasyonu | Python betiği | 43 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 7 | `10_05_01_loss-fonksiyonlarinin-python-ile-karsilastirmali.py` | Kod 10.5 | 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması → Loss Fonksiyonlarının Python ile Karşılaştırmalı Uygulaması | Python betiği | 39 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 8 | `10_05_02_ogrenme-orani-cizelgeleme.py` | Kod 10.6 | 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması → Öğrenme Oranı Çizelgeleme (Learning Rate Scheduling) | Python betiği | 68 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 9 | `10_05_03_geri-yayilim-sifirdan-numpy-implementasyonu.py` | Kod 10.7 | 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması → Geri Yayılım: Sıfırdan NumPy Implementasyonu | Python betiği | 52 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 10 | `10_06_01_tensorler-tensorflow-un-temel-veri-yapisi.py` | Kod 10.8 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Tensörler: TensorFlow'un Temel Veri Yapısı | Python betiği | 20 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 11 | `10_06_02_adim-1-katmanlarin-insasi.py` | Kod 10.9 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Adım 1: Katmanların İnşası (Model Architecture) | Python betiği | 23 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 12 | `10_06_02_adim-2-modeli-derleme.py` | Kod 10.10 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Adım 2: Modeli Derleme (model.compile) | Python betiği | 27 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 13 | `10_06_02_adim-3-modeli-egitme-ve-callback-ler.py` | Kod 10.11 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Adım 3: Modeli Eğitme (model.fit) ve Callback'ler | Python betiği | 36 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 14 | `10_06_02_functional-api-residual-baglanti-ornegi.py` | Kod 10.12 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Functional API: Residual Bağlantı Örneği | Python betiği | 18 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 15 | `10_06_03_bonus-iris-veri-seti-ile-mlp-regresyon-ve-sinifl.py` | Kod 10.15 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Bonus: Iris Veri Seti ile MLP Regresyon ve Sınıflandırma Karşılaştırması | Python betiği | 40 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 16 | `10_06_03_model-performans-analizi-hatali-tahminlerin-ince.py` | Kod 10.14 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → Model Performans Analizi: Hatalı Tahminlerin İncelenmesi | Python betiği | 22 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |
| 17 | `10_06_03_ornek-proje-mnist-ile-uctan-uca-goruntu-siniflan.py` | Kod 10.13 | 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması → 10.6.3. Örnek Proje: MNIST ile Uçtan Uca Görüntü Sınıflandırma | Python betiği | 123 | [▶](https://colab.research.google.com/github/rtekin-lab/VM-ML/blob/main/kod/notebooks/bolum10.ipynb) |

---

> Bu dosyalar kitaptaki kod bloklarından üretilmiştir. Her dosya tek başına
> çalışacak biçimde düzenlenmiş, kitapta önceki bloklarda kalan `import`
> satırları dosya başına eklenmiştir.
