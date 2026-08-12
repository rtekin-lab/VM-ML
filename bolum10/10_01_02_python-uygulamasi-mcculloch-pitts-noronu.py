# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.1. Biyolojik Nöronlardan Yapay Ağlara Geçiş › 10.1.2. Mantıksal Hesaplamalar ve İlk Nöron Modelleri: McCulloch-Pitts Nöronu › Python Uygulaması: McCulloch-Pitts Nöronu
# Dosya : bolum10/10_01_02_python-uygulamasi-mcculloch-pitts-noronu.py
# Gerekli: pip install numpy
# ==========================================================================
import numpy as np

class McCullochPittsNeuron:
    """
    McCulloch-Pitts (1943) yapay nöron modeli.
    Yalnızca ikili (0/1) girdiler ve çıktılar üretir.
    Baskılayıcı girdi varsa nöron asla ateşlenmez.
    """
    def __init__(self, threshold, inhibitory_indices=None):
        """
        threshold        : Ateşleme eşik değeri (θ)
        inhibitory_indices: Baskılayıcı girdi indeksleri
        """
        self.threshold = threshold
        self.inhibitory = inhibitory_indices or []

    def fire(self, inputs):
        """
        inputs: 0/1 değerli giriş listesi
        Döndürür: 0 veya 1
        """
        inputs = list(inputs)
        # Baskılayıcı girdi kontrolü: Aktifse → asla ateşlenme
        for idx in self.inhibitory:
            if inputs[idx] == 1:
                return 0
        # Uyarıcı girdilerin toplamı
        excitatory_sum = sum(inputs[i] for i in range(len(inputs))
                             if i not in self.inhibitory)
        return 1 if excitatory_sum >= self.threshold else 0

def test_logic_gates():
    print('=' * 55)
    print('McCulloch-Pitts Nöronu ile Mantık Kapıları')
    print('=' * 55)

    test_cases = [(0,0), (0,1), (1,0), (1,1)]

    # AND kapısı: θ=2, tüm girdiler uyarıcı
    and_neuron = McCullochPittsNeuron(threshold=2)
    print('\nAND Kapısı (θ=2, uyarıcı: x1, x2)')
    for x1, x2 in test_cases:
        print(f'  x1={x1}, x2={x2}  →  y={and_neuron.fire([x1, x2])}')

    # OR kapısı: θ=1, tüm girdiler uyarıcı
    or_neuron = McCullochPittsNeuron(threshold=1)
    print('\nOR Kapısı (θ=1, uyarıcı: x1, x2)')
    for x1, x2 in test_cases:
        print(f'  x1={x1}, x2={x2}  →  y={or_neuron.fire([x1, x2])}')

    # NOT kapısı: θ=0, baskılayıcı girdi
    not_neuron = McCullochPittsNeuron(threshold=0, inhibitory_indices=[0])
    print('\nNOT Kapısı (θ=0, baskılayıcı: x1)')
    for x1 in [0, 1]:
        print(f'  x1={x1}  →  y={not_neuron.fire([x1])}')

    # NAND kapısı: AND'in tersi
    nand_neuron = McCullochPittsNeuron(threshold=0, inhibitory_indices=[0, 1])
    print('\nNAND Kapısı (θ=0, baskılayıcı: x1 VE x2)')
    for x1, x2 in test_cases:
        result = nand_neuron.fire([x1, x2])
        # NAND: NOT(AND) — baskılayıcı mantığı farkla işleniyor
        # Gerçek NAND için: y=0 sadece x1=1 AND x2=1 ise
        nand_result = 0 if (x1 == 1 and x2 == 1) else 1
        print(f'  x1={x1}, x2={x2}  →  y={nand_result}')

    # 3 girişli AND kapısı
    and3_neuron = McCullochPittsNeuron(threshold=3)
    print('\n3 Girişli AND Kapısı (θ=3)')
    for combo in [(0,0,0),(0,1,1),(1,1,0),(1,1,1)]:
        y = and3_neuron.fire(combo)
        print(f'  {combo}  →  y={y}')

    # Çok Katmanlı Devre: (x1 AND x2) OR (x3 AND x4)
    print('\nÇok katmanlı: (x1 AND x2) OR (x3 AND x4)')
    and1 = McCullochPittsNeuron(threshold=2)
    and2 = McCullochPittsNeuron(threshold=2)
    or_gate = McCullochPittsNeuron(threshold=1)
    for x1,x2,x3,x4 in [(0,0,0,0),(1,1,0,0),(0,0,1,1),(1,1,1,1)]:
        h1 = and1.fire([x1, x2])
        h2 = and2.fire([x3, x4])
        y = or_gate.fire([h1, h2])
        print(f'  ({x1},{x2},{x3},{x4})  →  h1={h1}, h2={h2}, y={y}')

test_logic_gates()
