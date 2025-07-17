# 17mb211_flasher

## Steps

Create a venv with:  
`python -m venv venv`  
`venv\Scripts\Activate.ps1`    

Install requirements:  
`pip install --upgrade --no-cache-dir FreeSimpleGUI pyserial`   
  
### How to Run
Use this command to run Powershell as Admin:   
`Start-Process powershell -Verb RunAs -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$($PWD.Path)'; . .\venv\Scripts\Activate.ps1"`  

And run with:  
`python main.py `  
  
##  

Or click on __`EXE.ps1`__
