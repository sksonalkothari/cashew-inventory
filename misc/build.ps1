# Build script for Cashew Inventory Installer
# This PowerShell script automates the installer build process

param(
    [string]$InnoSetupPath = "C:\Program Files (x86)\Inno Setup 6",
    [string]$OutputDir = ".\Output",
    [switch]$SkipCompile = $false,
    [switch]$OpenOutput = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cashew Inventory Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify Inno Setup installation
if (-not (Test-Path $InnoSetupPath)) {
    Write-Host "Error: Inno Setup not found at $InnoSetupPath" -ForegroundColor Red
    Write-Host "Please install Inno Setup 6.2+ from https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    exit 1
}

$isccPath = Join-Path $InnoSetupPath "ISCC.exe"
if (-not (Test-Path $isccPath)) {
    Write-Host "Error: ISCC.exe not found at $isccPath" -ForegroundColor Red
    exit 1
}

Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Green

# Check for required files
$requiredFiles = @(
    "CashewInventoryInstaller.iss",
    "launcher\AppLauncher.bat",
    "launcher\AppLauncher.vbs",
    "launcher\AppLauncher.ps1",
    "launcher\StopLauncher.bat",
    "launcher\setup_environment.bat"
)

foreach ($file in $requiredFiles) {
    $filePath = Join-Path (Get-Location) $file
    if (-not (Test-Path $filePath)) {
        Write-Host "Error: Missing required file: $file" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] All required files found" -ForegroundColor Green
Write-Host ""

# Check for runtimes
Write-Host "[2/5] Checking runtime bundles..." -ForegroundColor Green

$runtimePaths = @{
    "Python 3.11" = "runtimes\python-3.11.5-embed-amd64"
    "Node.js"     = "runtimes\node-v24.13.1-win-x64"
}

foreach ($runtime in $runtimePaths.GetEnumerator()) {
    $path = Join-Path (Get-Location) $runtime.Value
    if (-not (Test-Path $path)) {
        Write-Host "[WARN] $($runtime.Key) not found at $($runtime.Value)" -ForegroundColor Yellow
        Write-Host "  The installer may fail if runtimes are not present." -ForegroundColor Yellow
    } else {
        Write-Host "[OK] $($runtime.Key) found" -ForegroundColor Green
    }
}
Write-Host ""

# Check backend requirements
Write-Host "[3/5] Checking backend preparation..." -ForegroundColor Green

$backendDir = "..\backend"
if (Test-Path (Join-Path $backendDir "requirements.txt")) {
    Write-Host "[OK] Backend requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "[WARN] Backend requirements.txt not found" -ForegroundColor Yellow
}

if (Test-Path (Join-Path $backendDir "app\main.py")) {
    Write-Host "[OK] Backend app found" -ForegroundColor Green
} else {
    Write-Host "Error: Backend app not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Auto-build frontend if dist missing
Write-Host "[4/5] Ensuring frontend build..." -ForegroundColor Green

$frontendDir = "..\frontend"
if (-not (Test-Path (Join-Path $frontendDir "dist"))) {
    Write-Host "Frontend dist not found. Attempting to build frontend..." -ForegroundColor Yellow
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Host "Error: npm is not available on PATH. Install Node.js or provide frontend/dist manually." -ForegroundColor Red
        exit 1
    }

    Push-Location -Path $frontendDir
    try {
        Write-Host "Running 'npm ci'..." -ForegroundColor Gray
        npm ci
        Write-Host "Running 'npm run build'..." -ForegroundColor Gray
        npm run build
    } finally {
        Pop-Location
    }

    if (-not (Test-Path (Join-Path $frontendDir "dist"))) {
        Write-Host "Error: frontend build did not produce dist/" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Frontend built successfully" -ForegroundColor Green
} else {
    Write-Host "[OK] Frontend dist build found (prebuilt)" -ForegroundColor Green
}
Write-Host ""

# Ensure backend venv exists
Write-Host "[5/5] Ensuring backend requirements installed..." -ForegroundColor Green

if (-not (Test-Path (Join-Path $backendDir "venv"))) {
    Write-Host "Backend venv not found. Creating and installing requirements..." -ForegroundColor Yellow

    if (Get-Command py -ErrorAction SilentlyContinue) {
        $pyExe = "py"
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pyExe = "python"
    } else {
        Write-Host "Error: Python not found. Install Python on build machine." -ForegroundColor Red
        exit 1
    }

    Write-Host "Using Python: $pyExe" -ForegroundColor Gray

    Push-Location -Path $backendDir
    try {
        Write-Host "Creating virtual environment..." -ForegroundColor Gray
        & $pyExe -m venv venv
        
        Write-Host "Installing backend dependencies..." -ForegroundColor Gray
        & ".\venv\Scripts\pip.exe" install --upgrade pip
        & ".\venv\Scripts\pip.exe" install -r requirements.txt
    } finally {
        Pop-Location
    }

    if (-not (Test-Path (Join-Path $backendDir "venv"))) {
        Write-Host "Error: Backend venv not created" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Backend venv created and requirements installed" -ForegroundColor Green
} else {
    Write-Host "[OK] Backend venv already exists" -ForegroundColor Green
}
Write-Host ""

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "[OK] Output directory created: $OutputDir" -ForegroundColor Green
} else {
    Write-Host "[OK] Output directory exists: $OutputDir" -ForegroundColor Green
}
Write-Host ""

# Compile installer
if (-not $SkipCompile) {
    Write-Host "Compiling installer..." -ForegroundColor Green
    Write-Host "Using: $isccPath" -ForegroundColor Gray
    Write-Host ""
    
    $issFile = Join-Path (Get-Location) "CashewInventoryInstaller.iss"
    
    & $isccPath $issFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Installer compiled successfully!" -ForegroundColor Green
        
        $setupExe = Join-Path $OutputDir "CashewInventorySetup.exe"
        if (Test-Path $setupExe) {
            $size = (Get-Item $setupExe).Length / 1MB
            Write-Host "  Output: $setupExe" -ForegroundColor Cyan
            Write-Host "  Size: $([Math]::Round($size, 2)) MB" -ForegroundColor Cyan
            
            if ($OpenOutput) {
                Invoke-Item $OutputDir
            }
        }
    } else {
        Write-Host ""
        Write-Host "[ERROR] Compilation failed. Check the output above for errors." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping compilation (SkipCompile flag set)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Test the installer: Run Output\\CashewInventorySetup.exe" -ForegroundColor Gray
Write-Host "2. Verify the app starts/stops correctly via AppLauncher.vbs" -ForegroundColor Gray
Write-Host "3. Check logs in %USERPROFILE%\\CashewInventoryLogs" -ForegroundColor Gray
Write-Host ""