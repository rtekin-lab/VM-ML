# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.5. Derin Ogrenme Tabanlı Anomali Tespit Yontemleri › 3.3.5.1. Autoencoder Tabanlı Anomali Tespiti
# Kitap  : Kod 3.35 (Autoencoder ile zaman serisi anomali tespiti)
# Dosya : bolum03/03_03_05_01_autoencoder-tabanli-anomali-tespiti.py
# Gerekli: pip install matplotlib numpy torch
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Autoencoder ile Zaman Serisi Anomali Tespiti
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

torch.manual_seed(42); np.random.seed(42)
t = np.linspace(0, 100, 2000)
ts = np.sin(2*np.pi*t/10) + np.sin(2*np.pi*t/3) + np.random.normal(0,0.2,len(t))
anom_idx = np.random.choice(range(500,1800),10,replace=False)
ts_anom = ts.copy(); ts_anom[anom_idx] += np.random.uniform(3,5,10)

window = 30
X_w = np.array([ts[i:i+window] for i in range(len(ts)-window)], dtype=np.float32)
X_t = torch.FloatTensor(X_w)

class AE(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(30,16),nn.ReLU(),nn.Linear(16,6),nn.ReLU())
        self.dec = nn.Sequential(nn.Linear(6,16),nn.ReLU(),nn.Linear(16,30))
    def forward(self,x): return self.dec(self.enc(x))

model = AE()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
ldr = DataLoader(TensorDataset(X_t), batch_size=64, shuffle=True)
model.train()
for ep in range(50):
    tot=0
    for (b,) in ldr:
        r=model(b); l=nn.MSELoss()(r,b)
        opt.zero_grad(); l.backward(); opt.step(); tot+=l.item()
    if (ep+1)%10==0: print("Epoch {}: {:.6f}".format(ep+1,tot/len(ldr)))

model.eval()
with torch.no_grad():
    yeniden = model(X_t)
    hatalar = ((X_t-yeniden)**2).mean(dim=1).numpy()
esik = np.percentile(hatalar, 95)
print("Esik (95.yuzdelik): {:.6f}".format(esik))
print("Anomali sayisi: {}".format((hatalar>esik).sum()))
