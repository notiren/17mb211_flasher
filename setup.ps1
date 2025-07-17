# Helper: Write in color
function Write-Info($msg)       { Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Write-ErrorExit($msg)  { Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

# Optional: Warn if script execution is restricted
$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($currentPolicy -eq "Restricted") {
    Write-Host ""
    Write-Host "   Your execution policy is 'Restricted' and may prevent this script from running." -ForegroundColor Yellow
    Write-Host "   To fix: run this command in PowerShell and restart the script:" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Step 1: Check if Python is available
Write-Info "Checking for Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-ErrorExit "Python is not installed or not in PATH. Please install Python first."
}

# Step 2: Create virtual environment
if (-not (Test-Path ".\venv")) {
    Write-Info "Creating virtual environment in .\venv..."
    python -m venv venv
    if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
        Write-ErrorExit "Failed to create virtual environment."
    }
} else {
    Write-Info "venv already exists. Skipping creation."
}

# Step 3: Activate venv in current session
Write-Info "Activating venv temporarily to install packages..."
. .\venv\Scripts\Activate.ps1

# Step 4: Install required packages
Write-Info "Installing required packages..."
pip install --upgrade --no-cache-dir FreeSimpleGUI pyserial
if ($LASTEXITCODE -ne 0) {
    Write-ErrorExit "Package installation failed."
}

# Done
Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Cyan
Write-Host "To run the app, double-click on:" -ForegroundColor Cyan
Write-Host ""
Write-Host " >> EXE.ps1" -ForegroundColor Blue
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
[void][System.Console]::ReadKey($true)
