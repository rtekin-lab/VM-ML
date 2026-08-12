# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma › Bölüm şekilleri
# Dosya : bolum06/06_00_bolum-sekilleri.py
# Gerekli: pip install numpy matplotlib scikit-learn
# ==========================================================================
"""Bölüm 6'nın kavramsal ve uygulamalı şekillerini üretir."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.inspection import permutation_importance

plt.rcParams['font.size'] = 9
CM = ListedColormap(['#E8907E', '#7EA6E8'])
CMB = ListedColormap(['#F7DCD6', '#D9E4F5'])


# --- Şekil 1: Sigmoid fonksiyonu ve karar eşiği -------------------------
def sigmoid_sekli():
    z = np.linspace(-8, 8, 400)
    s = 1 / (1 + np.exp(-z))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
    a1.plot(z, s, color='#1F3864', linewidth=2)
    a1.axhline(0.5, color='#C0392B', linestyle='--', linewidth=1)
    a1.axvline(0, color='gray', linewidth=0.8)
    a1.fill_between(z, 0, s, where=(z > 0), alpha=0.12, color='#2E5A8A')
    a1.set_xlabel('z = β₀ + β₁x'); a1.set_ylabel('σ(z) = P(y=1|x)')
    a1.set_title('Sigmoid bağlantı fonksiyonu'); a1.grid(alpha=0.3)
    a1.annotate('karar eşiği 0.5', xy=(0, 0.5), xytext=(2.5, 0.28),
                arrowprops=dict(arrowstyle='->', color='#C0392B'), color='#C0392B')

    p = np.linspace(0.001, 0.999, 400)
    a2.plot(p, -np.log(p), label='y = 1 ise  −log(p̂)', color='#1F3864', linewidth=2)
    a2.plot(p, -np.log(1 - p), label='y = 0 ise  −log(1−p̂)', color='#C0392B',
            linewidth=2, linestyle='--')
    a2.set_xlabel('Tahmin edilen olasılık p̂'); a2.set_ylabel('Kayıp')
    a2.set_title('Log-kayıp (çapraz entropi)'); a2.set_ylim(0, 5)
    a2.legend(fontsize=8); a2.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


# --- Şekil 2: Üç temel sınıflandırıcının karar sınırları ----------------
def karar_sinirlari():
    X, y = make_moons(n_samples=300, noise=0.28, random_state=42)
    X = StandardScaler().fit_transform(X)
    modeller = [('Lojistik Regresyon', LogisticRegression()),
                ('KNN (k=15)', KNeighborsClassifier(15)),
                ('Gaussian Naive Bayes', GaussianNB())]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - .5, X[:, 0].max() + .5, 300),
                         np.linspace(X[:, 1].min() - .5, X[:, 1].max() + .5, 300))
    for ax, (ad, m) in zip(axes, modeller):
        m.fit(X, y)
        Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=CMB, alpha=0.9)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=CM, s=18, edgecolor='k', linewidth=0.3)
        ax.set_title(f'{ad}\nDoğruluk = {m.score(X, y):.3f}')
        ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout(); plt.show()


# --- Şekil 3: KNN'de k değerinin etkisi ---------------------------------
def knn_k_etkisi():
    X, y = make_moons(n_samples=300, noise=0.3, random_state=1)
    X = StandardScaler().fit_transform(X)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)
    ks = [1, 5, 25, 99]
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.8))
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - .5, X[:, 0].max() + .5, 250),
                         np.linspace(X[:, 1].min() - .5, X[:, 1].max() + .5, 250))
    for ax, k in zip(axes, ks):
        m = KNeighborsClassifier(k).fit(Xtr, ytr)
        Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=CMB, alpha=0.9)
        ax.scatter(Xtr[:, 0], Xtr[:, 1], c=ytr, cmap=CM, s=14, edgecolor='k', linewidth=0.3)
        ax.set_title(f'k = {k}\nEğitim {m.score(Xtr, ytr):.2f} | Test {m.score(Xte, yte):.2f}')
        ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout(); plt.show()


# --- Şekil 4: Safsızlık ölçütleri ---------------------------------------
def safsizlik():
    p = np.linspace(0.001, 0.999, 400)
    entropi = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    gini = 2 * p * (1 - p)
    hata = np.minimum(p, 1 - p)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(p, entropi, label='Entropi', color='#1F3864', linewidth=2)
    ax.plot(p, gini, label='Gini safsızlığı', color='#C0392B', linewidth=2, linestyle='--')
    ax.plot(p, hata, label='Sınıflandırma hatası', color='#27AE60', linewidth=1.8, linestyle=':')
    ax.set_xlabel('p (birinci sınıfın oranı)'); ax.set_ylabel('Safsızlık')
    ax.set_title('Bölünme ölçütlerinin karşılaştırması')
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


# --- Şekil 5: Karar ağacı ve budamanın etkisi ---------------------------
def karar_agaci():
    veri = load_breast_cancer()
    Xtr, Xte, ytr, yte = train_test_split(veri.data, veri.target,
                                          test_size=0.3, random_state=42, stratify=veri.target)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5),
                                 gridspec_kw={'width_ratios': [1.35, 1]})
    agac = DecisionTreeClassifier(max_depth=3, random_state=42).fit(Xtr, ytr)
    plot_tree(agac, ax=a1, feature_names=veri.feature_names, class_names=['kötü huylu', 'iyi huylu'],
              filled=True, impurity=False, fontsize=6, proportion=True)
    a1.set_title('Derinliği 3 ile sınırlanmış karar ağacı')

    derinlikler = range(1, 21)
    egt, tst = [], []
    for dd in derinlikler:
        m = DecisionTreeClassifier(max_depth=dd, random_state=42).fit(Xtr, ytr)
        egt.append(m.score(Xtr, ytr)); tst.append(m.score(Xte, yte))
    a2.plot(derinlikler, egt, 'o-', label='Eğitim', color='#1F3864')
    a2.plot(derinlikler, tst, 's--', label='Test', color='#C0392B')
    a2.set_xlabel('Ağaç derinliği'); a2.set_ylabel('Doğruluk')
    a2.set_title('Derinlik arttıkça aşırı öğrenme')
    a2.legend(); a2.grid(alpha=0.3); a2.set_xticks(range(1, 21, 2))
    plt.tight_layout(); plt.show()


# --- Şekil 6: OOB hatasının yakınsaması ---------------------------------
def oob_yakinsama():
    veri = load_breast_cancer()
    X, y = veri.data, veri.target
    n_araligi = list(range(5, 305, 10))
    oob = []
    for n in n_araligi:
        rf = RandomForestClassifier(n_estimators=n, oob_score=True,
                                    random_state=42, n_jobs=-1).fit(X, y)
        oob.append(1 - rf.oob_score_)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(n_araligi, oob, '-o', markersize=3, color='#1F3864')
    ax.set_xlabel('Ağaç sayısı'); ax.set_ylabel('OOB hatası')
    ax.set_title('Random Forest: OOB hatasının ağaç sayısıyla yakınsaması')
    ax.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


# --- Şekil 7: ROC eğrileri ve öznitelik önemleri ------------------------
def roc_ve_onem():
    veri = load_breast_cancer()
    Xtr, Xte, ytr, yte = train_test_split(veri.data, veri.target,
                                          test_size=0.3, random_state=42, stratify=veri.target)
    modeller = [('Lojistik Regresyon', LogisticRegression(max_iter=5000)),
                ('Karar Ağacı', DecisionTreeClassifier(max_depth=4, random_state=42)),
                ('Random Forest', RandomForestClassifier(n_estimators=200, random_state=42)),
                ('AdaBoost', AdaBoostClassifier(random_state=42)),
                ('Gradient Boosting', GradientBoostingClassifier(random_state=42))]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.8))
    Xtr_s = StandardScaler().fit(Xtr)
    for ad, m in modeller:
        Xa, Xb = (Xtr_s.transform(Xtr), Xtr_s.transform(Xte)) if 'Lojistik' in ad else (Xtr, Xte)
        m.fit(Xa, ytr)
        skor = m.predict_proba(Xb)[:, 1]
        fpr, tpr, _ = roc_curve(yte, skor)
        a1.plot(fpr, tpr, linewidth=1.8, label=f'{ad} (AUC={auc(fpr, tpr):.3f})')
    a1.plot([0, 1], [0, 1], 'k--', linewidth=0.9)
    a1.set_xlabel('Yanlış pozitif oranı'); a1.set_ylabel('Doğru pozitif oranı')
    a1.set_title('ROC eğrileri'); a1.legend(fontsize=7.5, loc='lower right'); a1.grid(alpha=0.3)

    rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(Xtr, ytr)
    perm = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=42)
    sira = perm.importances_mean.argsort()[-12:]
    a2.barh(range(len(sira)), perm.importances_mean[sira],
            xerr=perm.importances_std[sira], color='#2E5A8A')
    a2.set_yticks(range(len(sira)))
    a2.set_yticklabels([veri.feature_names[i] for i in sira], fontsize=7.5)
    a2.set_xlabel('Permütasyon önemi')
    a2.set_title('Random Forest öznitelik önemleri (permütasyon)')
    a2.grid(alpha=0.3, axis='x')
    plt.tight_layout(); plt.show()


if __name__ == '__main__':
    sigmoid_sekli()
    karar_sinirlari()
    knn_k_etkisi()
    safsizlik()
    karar_agaci()
    oob_yakinsama()
    roc_ve_onem()
