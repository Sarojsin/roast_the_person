# Setup script for Roast My Profile
# Uses system 'python' command

$ErrorActionPreference = "Stop"

Write-Host "Checking Python..." -ForegroundColor Cyan
try {
    $version = python --version 2>&1
    Write-Host "Found: $version" -ForegroundColor Green
}
catch {
    Write-Host "Error: 'python' command not found." -ForegroundColor Red
    exit 1
}

# 1. Create Virtual Environment
Write-Host "`n[1/4] Creating Virtual Environment (.venv)..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "Removing existing .venv..."
    Remove-Item -Path ".venv" -Recurse -Force
}

python -m venv .venv
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Error: Failed to create .venv" -ForegroundColor Red
    exit 1
}

# 2. Install Backend Dependencies
Write-Host "`n[2/4] Installing Backend Dependencies..." -ForegroundColor Cyan
$venvPython = ".\.venv\Scripts\python.exe"

# Upgrade pip
Write-Host "Upgrading pip..."
& $venvPython -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements from backend\requirements.txt..."
# Try installing without deps first to see if it works, then with deps? No, standard install.
# We use --prefer-binary to avoid building from source if possible
& $venvPython -m pip install -r backend\requirements.txt --prefer-binary

# 3. Install Frontend Dependencies
Write-Host "`n[3/4] Installing Frontend Dependencies..." -ForegroundColor Cyan
if (Test-Path "frontend\package.json") {
    Push-Location frontend
    npm install
    Pop-Location
}
else {
    Write-Host "frontend\package.json not found, skipping..." -ForegroundColor Yellow
}

# 4. Create Run Script
Write-Host "`n[4/4] Creating Run Script (run_app.ps1)..." -ForegroundColor Cyan
$runScript = @"
# Start Backend
Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& { . .\.venv\Scripts\Activate.ps1; cd backend; python -m app.main }"

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& { cd frontend; npm run dev }"

Write-Host "App is starting! Check the opened windows." -ForegroundColor Cyan
"@
Set-Content -Path "run_app.ps1" -Value $runScript

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "To start the app, run: .\run_app.ps1" -ForegroundColor Yellow
