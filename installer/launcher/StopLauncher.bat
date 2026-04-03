@echo off
REM Stop backend and frontend processes (process mode)

echo Stopping Cashew Inventory processes...
taskkill /IM python.exe /F >nul 2>&1

if errorlevel 1 (
    echo No Python processes found.
) else (
    echo Backend and frontend stopped.
)

echo.
echo All processes stopped.
echo.