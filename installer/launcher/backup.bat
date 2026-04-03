@echo off
set APP_DIR=%~1
set BACKUP_DIR=%~2

echo Creating backup...

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Clean old backup
rmdir /s /q "%BACKUP_DIR%\backend" >nul 2>&1
rmdir /s /q "%BACKUP_DIR%\frontend" >nul 2>&1

REM Backup backend
xcopy "%APP_DIR%\backend" "%BACKUP_DIR%\backend\" /E /I /Y >nul

REM Backup frontend
xcopy "%APP_DIR%\frontend" "%BACKUP_DIR%\frontend\" /E /I /Y >nul

echo Backup completed
exit /b 0