@echo off
setlocal

set "APP_DIR=%~1"
if "%APP_DIR%"=="" set "APP_DIR=%~dp0.."

set "BACKEND_DIR=%APP_DIR%\backend"
set "FRONTEND_DIST=%ProgramData%\CashewInventory\frontend\dist"
set "PYTHON_EXE=%APP_DIR%\python\python.exe"
set "LOGS_DIR=%USERPROFILE%\CashewInventoryLogs"

if not exist "%LOGS_DIR%" mkdir "%LOGS_DIR%"

echo Starting Backend...
pushd "%BACKEND_DIR%"
start "Backend" "%PYTHON_EXE%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 >> "%LOGS_DIR%\backend.log" 2>&1
popd

echo Starting Frontend...
pushd "%FRONTEND_DIST%"
start "Frontend" "%PYTHON_EXE%" -m http.server 5173 >> "%LOGS_DIR%\frontend.log" 2>&1
popd

timeout /t 3 /nobreak >nul
echo Launching browser...
start "" http://127.0.0.1:5173

echo Done. Logs are in %LOGS_DIR%.