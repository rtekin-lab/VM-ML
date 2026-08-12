# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.1. Kümeleme Analizi (Cluster Analysis) › 7.1.3. Yoğunluk Tabanlı Yöntemler (DBSCAN) › Temel Kavramlar ve Matematiksel Tanımlar › DBSCAN Algoritması (Pseudocode)
# Dosya : bolum07/07_01_03_dbscan-algoritmasi.py
# ==========================================================================
# --- Algoritma: DBSCAN Pseudocode ---
def DBSCAN(D, eps, MinPts):
    labels = {p: UNDEFINED for p in D}
    cluster_id = 0

# --- Algoritma: DBSCAN Pseudocode ---
    for p in D:
        if labels[p] != UNDEFINED: continue  # Zaten işlendi

# --- Algoritma: DBSCAN Pseudocode ---
        neighbors = range_query(D, p, eps)    # ε-komşuluğu bul

# --- Algoritma: DBSCAN Pseudocode ---
        if len(neighbors) < MinPts:           # Çekirdek değil
            labels[p] = NOISE                 # Geçici gürültü
            continue

# --- Algoritma: DBSCAN Pseudocode ---
        # Yeni küme başlat
        cluster_id += 1
        labels[p] = cluster_id

# --- Algoritma: DBSCAN Pseudocode ---
        # Tüm ulaşılabilir noktaları kümeye ekle (BFS/DFS)
        seed_set = set(neighbors) - {p}
        while seed_set:
            q = seed_set.pop()
            if labels[q] == NOISE: labels[q] = cluster_id
            if labels[q] != UNDEFINED: continue
            labels[q] = cluster_id
            q_neighbors = range_query(D, q, eps)
            if len(q_neighbors) >= MinPts:
                seed_set |= set(q_neighbors)  # Çekirdek — genişlet

# --- Algoritma: DBSCAN Pseudocode ---
    return labels
