# AppLauncher.ps1 - PowerShell launcher for Cashew Inventory

param(
    [string]$AppDir = "C:\Program Files\CashewInventory",
    [string]$Action = "start"
)

$BackendDir = Join-Path $AppDir "backend"
$FrontendDir = Join-Path $AppDir "frontend"
$PythonExe  = Join-Path $AppDir "python\python.exe"
$NpmExe     = Join-Path $AppDir "node\npm.cmd"
$LogsDir    = "$env:ProgramData\CashewInventory\logs"

if (!(Test-Path $LogsDir)) { New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null }

Write-Host "[DEBUG] APP_DIR: $AppDir"
Write-Host "[DEBUG] ACTION: $Action"
Write-Host "[DEBUG] PYTHON_EXE: $PythonExe"
Write-Host "[DEBUG] FRONTEND_DIR: $FrontendDir"
Write-Host "[DEBUG] LOGS_DIR: $LogsDir"
Write-Host ""

switch ($Action.ToLower()) {
    "start" {
        if (Test-Path $PythonExe) {
            Write-Host "Starting Backend..."
            Start-Process -FilePath $PythonExe `
                -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000" `
                -WorkingDirectory $BackendDir `
                -RedirectStandardOutput "$LogsDir\backend.log" `
                -RedirectStandardError "$LogsDir\backend.log"

            if (Test-Path $NpmExe) {
                Write-Host "Starting Frontend..."
                Start-Process -FilePath $NpmExe `
                    -ArgumentList "run preview" `
                    -WorkingDirectory $FrontendDir `
                    -RedirectStandardOutput "$LogsDir\frontend.log" `
                    -RedirectStandardError "$LogsDir\frontend.log"
            } else {
                Write-Warning "npm not found, skipping frontend startup"
                if (Test-Path "$FrontendDir\dist\index.html") {
                    Start-Process "$FrontendDir\dist\index.html"
                }
            }

            Start-Sleep -Seconds 3
            Write-Host "Launching browser..."
            Start-Process "http://127.0.0.1:8000"
        } else {
            Write-Error "Python not found at $PythonExe"
        }
    }
    "stop" {
        Write-Host "Stopping Backend..."
        Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
        Write-Host "Stopping Frontend..."
        Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
    }
    "status" {
        Get-Process -Name "python" -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Host "Backend is running"
        }
        Get-Process -Name "node" -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Host "Frontend is running"
        }
    }
    default {
        Write-Host "Usage: .\AppLauncher.ps1 -AppDir <path> -Action start|stop|status"
    }
}