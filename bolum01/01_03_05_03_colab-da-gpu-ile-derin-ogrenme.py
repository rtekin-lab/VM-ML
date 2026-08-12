# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.5. Google Colaboratory (Colab) › 1.3.5.3. Colab'da GPU ile Derin Ogrenme
# Kitap  : Kod 1.80 (Google Colab GPU ortamında PyTorch ile sınır)
# Dosya : bolum01/01_03_05_03_colab-da-gpu-ile-derin-ogrenme.py
# Gerekli: pip install numpy torch
# ==========================================================================
# Google Colab: PyTorch ile GPU Egitimi
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import time

# GPU mevcut mu?
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Kullanilan cihaz: {device}")
if device.type == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Bellek: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Sentetik veri
torch.manual_seed(42)
n, d_in, d_out = 10_000, 50, 1
X = torch.randn(n, d_in)
y = X[:, :5].sum(dim=1, keepdim=True) + torch.randn(n, 1) * 0.5

ds = TensorDataset(X, y)
dl = DataLoader(ds, batch_size=256, shuffle=True)

# Model tanimla
model = nn.Sequential(
    nn.Linear(d_in, 128), nn.ReLU(), nn.BatchNorm1d(128),
    nn.Linear(128, 64),   nn.ReLU(), nn.BatchNorm1d(64),
    nn.Linear(64, d_out)
).to(device)

optimizer = optim.Adam(model.parameters(), lr=1e-3)
loss_fn   = nn.MSELoss()

# Egitim
baslangic = time.time()
for epoch in range(20):
    toplam = 0
    for xb, yb in dl:
        xb, yb = xb.to(device), yb.to(device)
        tahmin = model(xb)
        kayip = loss_fn(tahmin, yb)
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
        toplam += kayip.item()
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1:2d}: Kayip={toplam/len(dl):.4f}")

print(f"\nEgitim suresi: {time.time()-baslangic:.1f} sn ({device.type} uzerinde)")

# Modeli kaydet (Drive'a)
torch.save(model.state_dict(), "/content/drive/MyDrive/modeller/model.pth")
print("Model kaydedildi.")
