# Cashew Inventory Management - Installer Guide

This directory contains the installer scripts and configuration for building a Windows executable installer for the Cashew Inventory Management Application.

The installer is designed to be **simple, reliable, and update-friendly**. It does not install runtimes or dependencies; instead, it assumes the target system is already set up (from initial installation).

---

## Overview

- **Installer Type**: Inno Setup
- **Runtime Handling**: Uses existing Python environment (no installation)
- **Frontend**: Pre-built React (`dist/`) — no Node.js required
- **Setup Script**: Verifies environment and logs status
- **Logs Location**: `C:\ProgramData\CashewInventory\logs`
- **Installer Type**: Lightweight update installer

---

## Key Design Principles

- ✅ No runtime installation during setup
- ✅ No dependency installation (`pip install`)
- ✅ No Node.js required at runtime
- ✅ Fast and predictable installation
- ✅ Safe for updating existing installations

---

## Prerequisites (End User)

Before running the installer, the system must already have:

- Python 3.11 installed and working
- Required Python dependencies already installed
- Previous version of the application (recommended)

> ⚠️ This installer is intended for **updates**, not first-time setup.

---

## Directory Structure

```
installer/
├── CashewInventoryInstaller.iss
├── launcher/
│   ├── AppLauncher.vbs
│   ├── AppLauncher.bat
│   ├── AppLauncher.ps1
│   ├── setup_environment.bat
│   └── StopLauncher.bat
├── README.md
```

> Note: No runtimes (Python/Node) are included in this repository.

---

## Build Instructions

### Step 1: Build Frontend

```powershell
cd frontend
npm install
npm run build
```

This generates:

```
frontend/dist/
```

---

### Step 2: Verify Backend

Ensure your backend is ready:

- `requirements.txt` is up to date
- No breaking dependency changes

---

### Step 3: Compile Installer

1. Open **Inno Setup Compiler**
2. Open `CashewInventoryInstaller.iss`
3. Click **Build → Compile**

Output:

```
installer/Output/CashewInventorySetup.exe
```

---

## Installation (End User)

1. Run `CashewInventorySetup.exe` as **Administrator**
2. Follow the setup wizard
3. Installer will:
   - Copy backend files
   - Copy frontend build (`dist`)
   - Create logs directory
   - Run environment verification script
   - Create shortcuts

---

## Environment Verification

During installation, `setup_environment.bat` will:

- ✅ Verify Python runtime
- ✅ Check Python dependencies (`pip check`)
- ✅ Verify frontend build exists
- ✅ Verify backend files exist
- ✅ Generate logs

---

## Logs

Logs are stored at:

```
C:\ProgramData\CashewInventory\logs
```

Example:

```
setup_2026-04-03_14-30.log
```

Logs include:

- Environment validation results
- Errors and warnings
- Setup status

---

## Running the Application

- Use desktop shortcut: **Cashew Inventory**
- Uses a hidden launcher (VBS) to start/stop application

---

## Uninstallation

1. Go to **Control Panel → Programs**
2. Select **Cashew Inventory Management**
3. Click **Uninstall**

The uninstaller:

- Removes application files
- Removes shortcuts

> Logs in `ProgramData` are preserved for debugging

---

## Troubleshooting

### Application fails after update

- Check logs:

  ```
  C:\ProgramData\CashewInventory\logs
  ```

- Verify Python dependencies:

  ```
  python -m pip check
  ```

---

### Missing dependencies

If dependencies changed between versions:

```powershell
cd backend
pip install -r requirements.txt
```

---

### Frontend not loading

- Ensure `frontend/dist/index.html` exists
- Rebuild frontend if needed:

  ```powershell
  npm run build
  ```

---

### Python not found

- Ensure Python is installed and accessible
- Verify:

  ```powershell
  python --version
  ```

---

## Important Notes

- This installer **does not install Python or dependencies**
- It assumes a **pre-configured environment**
- Ideal for:
  - Internal deployments
  - Existing customers
  - Controlled environments

---

## Future Enhancements (Optional)

- Version-aware upgrades
- Database migration handling
- Full installer (for new users)

---

## Version

**Installer Version**: 1.0.0
**Last Updated**: April 2026

---
