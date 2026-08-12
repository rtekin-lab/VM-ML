# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ › 8.1. Birliktelik Kuralları (Association Rules) › 8.1.2. Algoritmalar: Apriori ve FP-Growth › Python Uygulaması — Kapsamlı Birliktelik Kuralı Analizi
# Kitap  : Kod 8.1 (Kapsamlı birliktelik kuralı analizi: destek,) · Kod 8.2 (FP-Growth ile sık öğe kümesi bulma)
# Dosya : bolum08/08_01_02_python-uygulamasi-kapsamli-birliktelik-kurali-an.py
# Gerekli: pip install matplotlib mlxtend numpy pandas seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# --- Python: Veri Hazırlama ve One-Hot Encoding ---
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import matplotlib.pyplot as plt
import time

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
# ─── 1. Gerçekçi Market Sepeti Veri Seti ─────────────────────────
# 1000 işlemli sentetik market verisi oluştur
np.random.seed(42)

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
urunler = ["Ekmek", "Süt", "Tereyağı", "Yumurta", "Peynir",
           "Zeytin", "Reçel", "Çay", "Kahve", "Bisküvi",
           "Makarna", "Domates Salçası", "Zeytinyağı", "Pirinç"]

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
# Gerçekçi sepet kalıpları tanımla
patterns = [
    ["Ekmek", "Süt", "Tereyağı"],          # Kahvaltı seti
    ["Ekmek", "Yumurta", "Peynir", "Zeytin"],
    ["Makarna", "Domates Salçası", "Zeytinyağı"],  # Yemek seti
    ["Çay", "Bisküvi"],
    ["Kahve", "Süt"],
    ["Pirinç", "Domates Salçası"],
]

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
dataset = []
for _ in range(1000):
    # Her işlem için 1-2 kalıp + rastgele ürünler
    sepet = set()
    for pattern in np.random.choice(len(patterns),
                                    size=np.random.randint(1, 3),
                                    replace=False):
        sepet.update(patterns[pattern])
    # Ek rastgele ürünler ekle (gürültü)
    n_extra = np.random.randint(0, 3)
    sepet.update(np.random.choice(urunler, n_extra, replace=False))
    dataset.append(list(sepet))

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
# ─── 2. TransactionEncoder ile One-Hot Encoding ───────────────────
te = TransactionEncoder()
te_array = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_array, columns=te.columns_)

# --- Python: Veri Hazırlama ve One-Hot Encoding ---
print(f"Veri seti boyutu: {df.shape}")
print(f"Öğe sayısı: {len(te.columns_)}")
print(f"Ortalama sepet boyutu: {df.sum(axis=1).mean():.2f} ürün")
print("\nİlk 3 işlem:")
print(df.head(3).T)

# --- Python: Apriori vs FP-Growth Performans Karşılaştırması ---
# ─── 3. Apriori vs FP-Growth Karşılaştırması ─────────────────────
min_sup_values = [0.05, 0.08, 0.10, 0.15, 0.20]

# --- Python: Apriori vs FP-Growth Performans Karşılaştırması ---
results = []
for min_sup in min_sup_values:
    # Apriori
    t0 = time.time()
    fi_apriori = apriori(df, min_support=min_sup,
                         use_colnames=True, max_len=5)
    t_apriori = time.time() - t0

# --- Python: Apriori vs FP-Growth Performans Karşılaştırması ---
    # FP-Growth
    t0 = time.time()
    fi_fp = fpgrowth(df, min_support=min_sup,
                      use_colnames=True, max_len=5)
    t_fp = time.time() - t0

# --- Python: Apriori vs FP-Growth Performans Karşılaştırması ---
    results.append({
        "min_sup"       : min_sup,
        "fi_count"      : len(fi_fp),
        "t_apriori_ms"  : t_apriori * 1000,
        "t_fp_ms"       : t_fp * 1000,
    })

# --- Python: Apriori vs FP-Growth Performans Karşılaştırması ---
res_df = pd.DataFrame(results)
print("\n=== Apriori vs FP-Growth Performans Karşılaştırması ===")
print(f"{'min_sup':>8s} | {'Sık Küme':>9s} | {'Apriori(ms)':>12s} | {'FP-Growth(ms)':>14s}")
print("-" * 52)
for _, row in res_df.iterrows():
    print(f"{row.min_sup:>8.2f} | {row.fi_count:>9.0f} | {row.t_apriori_ms:>12.1f} | {row.t_fp_ms:>14.1f}")

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# ─── 4. FP-Growth ile Sık Öğe Kümesi Bulma ───────────────────────
frequent_itemsets = fpgrowth(
    df,
    min_support=0.07,      # En az %7 destek
    use_colnames=True,
    max_len=4)

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# Boyuta göre dağılım
frequent_itemsets["length"] = frequent_itemsets["itemsets"].apply(len)
print("Sık öğe kümesi boyut dağılımı:")
print(frequent_itemsets["length"].value_counts().sort_index())

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# ─── 5. Birliktelik Kuralları Çıkarma (Tüm Metrikler) ─────────────
rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.5)

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# Ek metrikler hesapla
rules["leverage"] = rules["support"] - (
    rules["antecedent support"] * rules["consequent support"])

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# Conviction hesapla
rules["conviction"] = np.where(
    rules["confidence"] == 1.0,
    np.inf,
    (1 - rules["consequent support"]) / (1 - rules["confidence"]))

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
print(f"\nToplam kural sayısı: {len(rules)}")
print("\n--- En İyi 10 Kural (Lift'e Göre) ---")
cols = ["antecedents", "consequents", "support",
        "confidence", "lift", "leverage", "conviction"]
print(rules[cols].sort_values("lift", ascending=False).head(10).to_string())

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# ─── 6. Kural Filtreleme Stratejileri ─────────────────────────────
# Strateji 1: Yüksek güven + yüksek lift
strong_rules = rules[
    (rules["confidence"] >= 0.7) &
    (rules["lift"] >= 1.5) &
    (rules["support"] >= 0.05)
].copy()
print(f"\nGüçlü Kural Sayısı (conf≥0.7, lift≥1.5): {len(strong_rules)}")

# --- Python: Birliktelik Kuralları Çıkarma ve Tüm Metrikler ---
# Strateji 2: Belirli bir ürün için öneriler (örn: Ekmek alanlara ne öner?)
ekmek_rules = rules[
    rules["antecedents"].apply(lambda x: "Ekmek" in str(x))
].sort_values("lift", ascending=False)
print("\nEkmek Alanlara Önerilen Ürünler:")
print(ekmek_rules[["antecedents","consequents","confidence","lift"]].head(5))

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
# ─── 7. Kural Görselleştirmesi ────────────────────────────────────
import matplotlib.pyplot as plt
import seaborn as sns

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
# Scatter: Support vs Confidence, renk=Lift
sc = axes[0].scatter(
    rules["support"], rules["confidence"],
    c=rules["lift"], cmap="RdYlGn",
    s=rules["lift"] * 20, alpha=0.7)
plt.colorbar(sc, ax=axes[0], label="Lift")
axes[0].set_xlabel("Destek (Support)")
axes[0].set_ylabel("Güven (Confidence)")
axes[0].set_title("Birliktelik Kuralları: Support vs Confidence")
axes[0].axhline(y=0.7, color="red", linestyle="--", alpha=0.5, label="min_conf=0.7")
axes[0].legend()

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
# Lift ısı haritası (tek ürün çiftleri)
single_ant = rules[rules["antecedents"].apply(lambda x: len(x)==1)]
single_both = single_ant[single_ant["consequents"].apply(lambda x: len(x)==1)]

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
if len(single_both) > 0:
    pivot = single_both.pivot_table(
        values="lift",
        index=single_both["antecedents"].apply(lambda x: list(x)[0]),
        columns=single_both["consequents"].apply(lambda x: list(x)[0]),
        aggfunc="max")
    sns.heatmap(pivot, ax=axes[1], cmap="YlOrRd",
                annot=True, fmt=".2f", linewidths=0.5)
    axes[1].set_title("Lift Isı Haritası (Tekli Öğe Çiftleri)")

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
plt.tight_layout()
plt.show()

# --- Python: Görselleştirme — Scatter Plot ve Isı Haritası ---
# ─── 8. Gerçek Veri: Online Retail Veri Seti (isteğe bağlı) ───────
# Büyük ölçekli gerçek veri için:
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
# df_retail = pd.read_excel(url)
# # Temizleme ve dönüşüm adımları...
# basket = df_retail.groupby(["InvoiceNo", "Description"])["Quantity"]\
#                   .sum().unstack().fillna(0)
# basket_bool = basket.applymap(lambda x: True if x > 0 else False)
# fi = fpgrowth(basket_bool, min_support=0.02, use_colnames=True)
# rules_retail = association_rules(fi, metric="lift", min_threshold=1.5)
# print(f"Kural sayısı: {len(rules_retail)}")
