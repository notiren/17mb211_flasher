# exe.ps1 - self-elevate, unblock, enter venv and run main.py

# If not running as admin, re-launch elevated (preserves the script path)
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
        [Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`""
    exit
}

# Ensure script runs from its folder
Set-Location -LiteralPath $PSScriptRoot

# Unblock the activate script (safe to run even if already unblocked)
if (Test-Path .\venv\Scripts\Activate.ps1) {
    try { Unblock-File .\venv\Scripts\Activate.ps1 -ErrorAction Stop } catch { }
}

# Prefer to call the venv python directly (avoids activation complexities)
$venvPython = Join-Path -Path $PSScriptRoot -ChildPath "venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    # Run main.py with the venv python
    & $venvPython (Join-Path $PSScriptRoot "main.py")
    $exitCode = $LASTEXITCODE
    exit $exitCode
}
else {
    # fallback: try activation then run python (keeps console env like interactive)
    . .\venv\Scripts\Activate.ps1
    python .\main.py
    exit $LASTEXITCODE
}
