# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.2. Farklı Veri Kaynakları ve Özellikleri › Sosyal Medya, Web ve Metin Verileri
# Kitap  : Kod 2.15 (BeautifulSoup ile web sayfasından tablo kazı)
# Dosya : bolum02/02_02_02_sosyal-medya-web-ve-metin-verileri.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# 1. Örnek Web İçerik Verisi (Sentetik)
documents = [
    "Veri madenciliği ve makine öğrenmesi geleceğin teknolojileridir.",
    "Web madenciliği içerik, yapı ve kullanım olarak ayrılır.",
    "Doğal dil işleme metin madenciliğinin bir alt dalıdır."
]

# 2. Metin Verisinin Vektörleştirilmesi (Bag of Words)
# Stop-words (ve, ile, bir vb.) temizliği bu aşamada yapılabilir
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# 3. Öznitelik Matrisinin Oluşturulması
word_freq_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

print("--- Kelime Frekans Matrisi ---")
print(word_freq_df.head())
