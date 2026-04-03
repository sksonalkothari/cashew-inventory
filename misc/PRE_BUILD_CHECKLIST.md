# Pre-Build Checklist

Use this checklist before building and distributing the Cashew Inventory installer.

## Before Building the Installer

### 1. Environment Setup

- [ ] Inno Setup 6.2+ installed
- [ ] Windows 10/11 machine with admin rights
- [ ] 500+ MB free disk space
- [ ] PowerShell 5.0+ available

### 2. Runtime Preparation

- [ ] Python 3.11 embeddable ZIP downloaded
- [ ] Python extracted to `installer\runtimes\python-3.11.5-embed-amd64\`
- [ ] Node.js portable ZIP downloaded
- [ ] Node.js extracted to `installer\runtimes\node-v20.11.0-win-x64\`
- [ ] NSSM binary downloaded
- [ ] NSSM extracted to `installer\runtimes\nssm-2.24-101-g897c7ad\win64\`
- [ ] All runtimes verified in place:
  ```powershell
  dir installer\runtimes
  dir installer\runtimes\python-3.11.5-embed-amd64\python.exe
  dir installer\runtimes\node-v20.11.0-win-x64\node.exe
  dir installer\runtimes\nssm-2.24-101-g897c7ad\win64\nssm.exe
  ```

### 3. Backend Preparation

- [ ] `backend\requirements.txt` exists and is up-to-date
- [ ] `backend\app\main.py` exists
- [ ] `backend\app\config.py` is properly configured
- [ ] All backend dependencies can be installed via pip
- [ ] No hardcoded absolute paths in backend config
- [ ] Database connection string uses environment variables or config

### 4. Frontend Preparation

- [ ] `frontend\package.json` exists
- [ ] All frontend dependencies installed: `npm install` (locally tested)
- [ ] Frontend builds successfully: `npm run build` (locally tested)
- [ ] `frontend\dist\` directory exists with production build
- [ ] `frontend\vite.config.ts` preview port is `5173`
- [ ] No hardcoded localhost:3000 references (use 5173)
- [ ] API base URL points to `http://localhost:8000` or uses environment variable

### 5. Application Files

- [ ] `resources\icon.ico` exists (256x256 minimum, OPTIONAL but recommended)
- [ ] `logs\` directory exists (empty is OK)
- [ ] `database\` directory with schema files exists (if needed for deployment)
- [ ] `.env.example` exists in backend (for documentation)
- [ ] No secrets/credentials in `app\config.py` (use env vars)

### 6. Installer Scripts

- [ ] `installer\CashewInventoryInstaller.iss` exists and is valid
- [ ] `installer\build.ps1` exists
- [ ] `installer\launcher\AppLauncher.bat` exists
- [ ] `installer\launcher\start_services.bat` exists
- [ ] `installer\launcher\stop_services.bat` exists
- [ ] `installer\launcher\install_services.bat` exists
- [ ] `installer\launcher\uninstall_services.bat` exists
- [ ] All batch files have Unix line endings (CRLF, not LF) if edited on Mac/Linux

### 7. Documentation

- [ ] `installer\README.md` reviewed and accurate
- [ ] `installer\QUICK_START.md` reviewed
- [ ] `installer\IMPLEMENTATION_SUMMARY.md` reviewed

## Building the Installer

### 8. Build Execution

- [ ] Run PowerShell as Administrator
- [ ] Navigate to `installer\` directory
- [ ] Execute: `.\build.ps1`
- [ ] Verify no errors in output
- [ ] Check for `Output\CashewInventorySetup.exe` creation
- [ ] Note the file size (should be ~120-150 MB)

**OR manually:**

- [ ] Open Inno Setup Compiler
- [ ] File → Open → `CashewInventoryInstaller.iss`
- [ ] Build → Compile
- [ ] Verify success message

## After Building

### 9. Pre-Deployment Testing (Recommended)

- [ ] Use a clean Windows VM or test machine (not development machine)
- [ ] Run installer with admin rights
- [ ] Verify extraction completes
- [ ] Verify services are installed (`services.msc`)
- [ ] Verify services auto-start
- [ ] Wait 5 seconds and verify both services show "Running"
- [ ] Verify browser opens to http://localhost:5173
- [ ] Verify frontend displays without errors
- [ ] Test login/basic functionality
- [ ] Check log files created:
  ```powershell
  dir "C:\Program Files\CashewInventory\logs\"
  type "C:\Program Files\CashewInventory\logs\backend.log"
  ```
- [ ] Verify no console windows appear
- [ ] Stop services via "Stop Application" shortcut
- [ ] Verify both services show "Stopped"
- [ ] Restart services via shortcut
- [ ] Verify application responds
- [ ] Uninstall application
- [ ] Verify services removed from `services.msc`
- [ ] Verify files removed from `C:\Program Files\CashewInventory\`
- [ ] Verify logs directory STILL EXISTS (not deleted)
- [ ] Verify shortcuts removed from Start Menu and Desktop

### 10. Code Signing (Optional, but Recommended)

- [ ] Obtain code signing certificate (or self-signed for testing)
- [ ] Sign `CashewInventorySetup.exe` with SignTool.exe
- [ ] Verify signature in file properties

### 11. Distribution Preparation

- [ ] Rename installer with version: `CashewInventorySetup-v1.0.0.exe`
- [ ] Calculate file hash for security:
  ```powershell
  Get-FileHash .\Output\CashewInventorySetup.exe
  ```
- [ ] Create release notes document
- [ ] Prepare installation instructions for end users (use QUICK_START.md as template)
- [ ] Host on download server or share via secure link

### 12. Final Verification Before Release

- [ ] Installer runs on Windows 10
- [ ] Installer runs on Windows 11
- [ ] Services start without errors
- [ ] Application is fully functional
- [ ] No security warnings on first run
- [ ] All shortcuts work correctly
- [ ] Uninstall is clean
- [ ] Logs are preserved after uninstall

## Troubleshooting During Build

| Error                    | Fix                                                                  |
| ------------------------ | -------------------------------------------------------------------- |
| ISCC.exe not found       | Verify Inno Setup installed at `C:\Program Files (x86)\Inno Setup 6` |
| "Missing required file"  | Check all launcher batch files exist in `installer\launcher\`        |
| Python runtime not found | Verify `runtimes\python-3.11.5-embed-amd64\python.exe` exists        |
| Node runtime not found   | Verify `runtimes\node-v20.11.0-win-x64\node.exe` exists              |
| NSSM not found           | Verify `runtimes\nssm-2.24-101-g897c7ad\win64\nssm.exe` exists       |
| Compilation fails        | Review error in Inno Setup compiler window, check ISS syntax         |

## Post-Build Troubleshooting

| Issue                | Check                                                              |
| -------------------- | ------------------------------------------------------------------ |
| Services don't start | `C:\Program Files\CashewInventory\logs\backend_error.log`          |
| Port already in use  | Kill existing processes: `netstat -ano \| findstr :8000`           |
| Browser doesn't open | Manually visit http://localhost:5173                               |
| API calls fail       | Check backend service status: `nssm status CashewInventoryBackend` |
| Database errors      | Verify Supabase connection string in `backend\app\config.py`       |

## Sign-Off

- **Prepared by**: ********\_******** Date: **\_\_\_**
- **Tested by**: ********\_******** Date: **\_\_\_**
- **Approved for release**: ********\_******** Date: **\_\_\_**

---

**Checklist Version**: 1.0  
**Last Updated**: February 2026
