@echo off
REM setup_environment.bat - Environment verification with logging

setlocal enabledelayedexpansion
set APP_DIR=%~1
set LOG_DIR=%~2

if "%APP_DIR%"=="" (
    echo [ERROR] No installation directory provided
    exit /b 1
)

if "%LOG_DIR%"=="" (
    set LOG_DIR=%ProgramData%\CashewInventory\logs
)

REM Create logs directory
set LOG_DIR=%ProgramData%\CashewInventory\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Create timestamped log file
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set DATE=%%d-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set TIME=%%a-%%b

set LOG_FILE=%LOG_DIR%\setup_%DATE%_%TIME%.log

echo =============================================== >> "%LOG_FILE%"
echo Cashew Inventory - Environment Verification >> "%LOG_FILE%"
echo =============================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Running environment checks...
echo Logs: %LOG_FILE%
echo.

REM -------------------------------
REM Python Check
REM -------------------------------
set PYTHON_EXE=%APP_DIR%\python\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python runtime not found >> "%LOG_FILE%"
    echo [ERROR] Python runtime not found at: %PYTHON_EXE%
    exit /b 1
)

echo [OK] Python runtime verified >> "%LOG_FILE%"
echo [OK] Python runtime verified

REM -------------------------------
REM Python dependencies Check
REM -------------------------------
echo Checking Python dependencies... >> "%LOG_FILE%"
echo Checking Python dependencies...

"%PYTHON_EXE%" -m pip check >nul 2>&1

if %ERRORLEVEL% neq 0 (
    echo [WARN] Some Python dependencies may be missing or incompatible
    echo [WARN] Please contact support or reinstall dependencies
) else (
    echo [OK] Python dependencies look good
)

REM -------------------------------
REM Frontend Check
REM -------------------------------
if exist "%APP_DIR%\frontend\dist\index.html" (
    echo [OK] Frontend build found >> "%LOG_FILE%"
    echo [OK] Frontend build found
) else (
    echo [WARN] Frontend dist missing >> "%LOG_FILE%"
    echo [WARN] Frontend dist folder missing
)

REM -------------------------------
REM Backend Check (basic)
REM -------------------------------
if exist "%APP_DIR%\backend" (
    echo [OK] Backend folder exists >> "%LOG_FILE%"
    echo [OK] Backend verified
) else (
    echo [ERROR] Backend missing >> "%LOG_FILE%"
    echo [ERROR] Backend folder missing
    exit /b 1
)

echo. >> "%LOG_FILE%"
echo [OK] Environment setup completed >> "%LOG_FILE%"

echo.
echo ===============================================
echo Setup completed successfully!
echo Logs saved at:
echo %LOG_FILE%
echo ===============================================

exit /b 0