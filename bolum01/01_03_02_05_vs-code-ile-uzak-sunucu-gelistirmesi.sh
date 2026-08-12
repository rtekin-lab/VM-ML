# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.2. Visual Studio Code (VS Code) › 1.3.2.5. VS Code ile Uzak Sunucu Geliştirmesi
# Kitap  : Kod 1.70 (VS Code Remote-SSH ile uzak GPU sunucusunda )
# Dosya : bolum01/01_03_02_05_vs-code-ile-uzak-sunucu-gelistirmesi.sh
# ==========================================================================
# 1. Uzantıyı yukle
code --install-extension ms-vscode-remote.remote-ssh

# 2. ~/.ssh/config dosyasina sunucu ekle
# Host veri-sunucusu
#     HostName 192.168.1.100
#     User kullanici
#     IdentityFile ~/.ssh/id_rsa
#     ForwardAgent yes

# 3. VS Code'da: F1 > "Remote-SSH: Connect to Host" > sunucu adi secin

# 4. Uzak sunucuda Python ortami olustur
ssh kullanici@192.168.1.100
python3 -m venv ~/.venv/gpu-proje
source ~/.venv/gpu-proje/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 5. VS Code'da uzak Python yorumlayicisini sec
# Ctrl+Shift+P > "Python: Select Interpreter"
# /home/kullanici/.venv/gpu-proje/bin/python secin

# 6. Port yonlendirme ile Jupyter uzerinde calis
# Uzak sunucuda:
jupyter lab --no-browser --port=8888
# VS Code otomatik olarak port yonlendirme olusturur
# Yerel tarayicida: http://localhost:8888 acin
