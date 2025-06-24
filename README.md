# 17mb211_flasher

Steps

python -m venv venv  
venv\Scripts\activate  
pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI pyserial
open Powershell as Admin or use this line:   
Start-Process powershell -Verb RunAs -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$($PWD.Path)'; . .\venv\Scripts\Activate.ps1"  
python main.py  

# Optional: create Executable

pip install pyinstaller  
pyinstaller main.spec  

Executable will be created in dist/ folder  
Run Exe as Administrator
