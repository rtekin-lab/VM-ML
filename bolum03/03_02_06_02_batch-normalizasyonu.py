# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.6. İleri Düzey Ölçeklendirme: QuantileTransformer ve Batch Normalizasyon › 3.2.6.2. Batch Normalizasyonu (Derin Öğrenme)
# Kitap  : Kod 3.27 (PyTorch ile Batch Normalization: eğitim hızı)
# Dosya : bolum03/03_02_06_02_batch-normalizasyonu.py
# Gerekli: pip install matplotlib torch
# ==========================================================================
# ─── PyTorch ile Batch Normalizasyonu Karşılaştırması ────────────
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

class MLP(nn.Module):
    def __init__(self, use_bn=False):
        super().__init__()
        layers = [nn.Linear(20, 64)]
        if use_bn: layers.append(nn.BatchNorm1d(64))
        layers += [nn.ReLU(), nn.Linear(64, 64)]
        if use_bn: layers.append(nn.BatchNorm1d(64))
        layers += [nn.ReLU(), nn.Linear(64, 1)]
        self.net = nn.Sequential(*layers)
    def forward(self, x): return self.net(x)

torch.manual_seed(42)
n, d = 500, 20
# Farklı ölçeklerde özellikler (büyük ölçek farkı)
# 10**i, i=19'da int64 sinirini asiyor (OverflowError). Olcek farki ayni,
# ama ussu float olarak ve makul araliginda uretiyoruz.
olcekler = torch.tensor([10.0 ** (i % 6) for i in range(d)])
X = torch.randn(n, d) * olcekler
y = X[:, 0] * 0.5 + X[:, 1] * 0.3 + torch.randn(n) * 0.1

def train(model, epochs=150, lr=1e-3):
    opt, loss_fn = torch.optim.Adam(model.parameters(), lr=lr), nn.MSELoss()
    losses = []
    for _ in range(epochs):
        opt.zero_grad()
        loss = loss_fn(model(X).squeeze(), y)
        loss.backward(); opt.step()
        losses.append(loss.item())
    return losses

l_normal = train(MLP(use_bn=False))
l_bn     = train(MLP(use_bn=True))

plt.figure(figsize=(9, 4))
plt.plot(l_normal, label="MLP (BatchNorm yok)", color="#e74c3c", alpha=0.8)
plt.plot(l_bn,     label="MLP + BatchNorm",     color="#2ecc71", alpha=0.8)
plt.xlabel("Epoch"); plt.ylabel("MSE Loss")
plt.title("Batch Normalizasyonu: Eğitim Hızı Karşılaştırması")
plt.legend(); plt.yscale("log"); plt.tight_layout(); plt.show()
