# 17mb211_flasher

Steps

python -m venv venv
venv\Scripts\activate
pip install -r req.txt
open powershell as admin with this line: 
Start-Process powershell -Verb RunAs -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$($PWD.Path)'; . .\venv\Scripts\Activate.ps1"
python main.py

# Optional: create Executable

python -m pip install pyinstaller
pyinstaller main.spec

Executable will be created in dist/ folder
