# 17mb211_flasher

## Steps

Create a venv with:  
`python -m venv venv`  
`venv\Scripts\Activate.ps1`    

Install requirements:  
`pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI pyserial`   
  
Open Powershell as Admin or use this line:   
`Start-Process powershell -Verb RunAs -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$($PWD.Path)'; . .\venv\Scripts\Activate.ps1"`  

Run with:  
`python main.py `  
  
Or click on __`EXE.ps1`__
