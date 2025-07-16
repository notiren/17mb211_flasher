Start-Process powershell -Verb RunAs -ArgumentList @(
    "-Command",
    @"
Set-Location -LiteralPath '$PWD';
. .\venv\Scripts\Activate.ps1;
python .\main.py
"@
)
