# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.2. Visual Studio Code (VS Code) › 1.3.2.1. Kurulum ve Ilk Yapilandirma
# Kitap  : Kod 1.68 (VS Code kurulumu ve temel Python uzantıları)
# Dosya : bolum01/01_03_02_01_kurulum-ve-ilk-yapilandirma.sh
# ==========================================================================
# 1. VS Code'u indirin: https://code.visualstudio.com/
#    Windows: .exe | macOS: .dmg / brew | Linux: .deb / .rpm / snap

# macOS (Homebrew ile)
brew install --cask visual-studio-code

# Linux (Ubuntu/Debian)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
     https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update && sudo apt install code

# 2. Temel Python uzantilari (VS Code icerisinden Ctrl+Shift+X)
# Zorunlu:
#   ms-python.python            — Temel Python destegi
#   ms-python.vscode-pylance    — Pylance dil sunucusu
#   ms-toolsai.jupyter          — Notebook destegi
# Onerilir:
#   ms-python.black-formatter   — Black kod formatlayici
#   charliermarsh.ruff          — Ruff linter (cok hizli)
#   ms-python.isort             — Import siralaici
#   visualstudioexptteam.vscodeintellicode  — AI tabanli tamamlama

# 3. Uzantilari komut satirindan yukle
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
