@echo off
setlocal EnableDelayedExpansion
title Cashew_Inventory_App_Start
set FRONTEND_DIR=%~dp0frontend
set BACKEND_DIR=%~dp0backend
set NODE_DIR=%~dp0node
set NODE_EXE=%NODE_DIR%\node.exe
set NPM_EXE=%NODE_DIR%\npm.cmd

echo Starting Cashew Inventory Management App...

:: Start Backend
echo Starting Backend Server...
start cmd /k "cd /d %BACKEND_DIR% && call venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000"

:: Start Frontend using local Node
echo Starting Frontend Server...
start cmd /k "cd /d %FRONTEND_DIR% && %NPM_EXE% run preview"

:: Bring the main command window to the front
powershell -command "(New-Object -ComObject WScript.Shell).AppActivate('Cashew_Inventory_App_Start')" >nul 2>&1

:: Wait for servers to be ready with active health checks
echo Waiting for servers to start...

set BACKEND_URL=
set FRONTEND_URL=
set MAX_ATTEMPTS=120
set ATTEMPT=0
set BACKEND_READY=0
set FRONTEND_READY=0

:health_check_loop
set /a ATTEMPT+=1
if %ATTEMPT% gtr %MAX_ATTEMPTS% goto health_check_timeout

:: Check backend on port 8000
if %BACKEND_READY% equ 0 (
    echo Checking Backend... ^(Attempt %ATTEMPT%/%MAX_ATTEMPTS%^)
    powershell -Command "(New-Object Net.Sockets.TcpClient).ConnectAsync('127.0.0.1', 8000).Wait(1000)" >nul 2>&1
    if !errorlevel! equ 0 (
        set BACKEND_URL=http://127.0.0.1:8000
        set BACKEND_READY=1
        echo Backend is ready at !BACKEND_URL!
    )
)

:: Check frontend on ports 4173 or 5173
if %FRONTEND_READY% equ 0 (
    echo Checking Frontend... ^(Attempt %ATTEMPT%/%MAX_ATTEMPTS%^)
    powershell -Command "(New-Object Net.Sockets.TcpClient).ConnectAsync('127.0.0.1', 4173).Wait(1000)" >nul 2>&1
    if !errorlevel! equ 0 (
        set FRONTEND_URL=http://localhost:4173
        set FRONTEND_READY=1
        echo Frontend is ready at !FRONTEND_URL!
        goto :health_check_complete
    )
    
    powershell -Command "(New-Object Net.Sockets.TcpClient).ConnectAsync('127.0.0.1', 5173).Wait(1000)" >nul 2>&1
    if !errorlevel! equ 0 (
        set FRONTEND_URL=http://localhost:5173
        set FRONTEND_READY=1
        echo Frontend is ready at !FRONTEND_URL!
        goto :health_check_complete
    )
)

:: If both ready, exit loop
if %BACKEND_READY% equ 1 if %FRONTEND_READY% equ 1 goto health_check_complete

:: Wait a bit before retrying
timeout /t 1 /nobreak >nul
goto health_check_loop

:health_check_timeout
echo WARNING: Servers did not start within expected time. Current status:
if %BACKEND_READY% equ 0 echo   - Backend: NOT READY
if %BACKEND_READY% equ 1 echo   - Backend: READY
if %FRONTEND_READY% equ 0 echo   - Frontend: NOT READY
if %FRONTEND_READY% equ 1 echo   - Frontend: READY

:health_check_complete

:: Launch browser with detected frontend URL
if defined FRONTEND_URL (
    echo Launching browser...
    start !FRONTEND_URL!
) else (
    echo Could not detect frontend URL. Please check server logs.
)

echo.
echo Servers started successfully!
if defined BACKEND_URL echo Backend: !BACKEND_URL!
if defined FRONTEND_URL echo Frontend: !FRONTEND_URL!
echo.

:: Bring the main command window to the front
powershell -command "(New-Object -ComObject WScript.Shell).AppActivate('start_app.bat')" >nul 2>&1

pause