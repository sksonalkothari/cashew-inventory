# Quick Start: Building & Testing the Installer

## Overview

This guide walks you through building the Cashew Inventory installer in **5 minutes**.

## Prerequisites

- **Inno Setup 6.2+** installed (download from [jrsoftware.org](https://jrsoftware.org/isdl.php))
- **Windows 10/11** with 500+ MB free disk space
- Admin rights on your machine

## Step-by-Step Build

### 1. Download and Extract Runtimes (~2 min)

Run PowerShell as Administrator and execute:

```powershell
cd C:\Users\Sonal\Workspace\CashewInventoryManagementApp\installer

# Create runtimes directory
mkdir runtimes -Force

# Download Python 3.11 embeddable (or download manually and extract)
# https://www.python.org/downloads/windows/ → "Windows embeddable package (64-bit)"
# Extract to: runtimes\python-3.11.5-embed-amd64\

# Download Node.js (or download manually and extract)
# https://nodejs.org/en/download/prebuilt-binaries → Windows (x64) binary zip
# Extract to: runtimes\node-v20.11.0-win-x64\

# Download NSSM (or download manually and extract)
# https://nssm.cc/download → Latest release, extract win64/nssm.exe
# Extract to: runtimes\nssm-2.24-101-g897c7ad\win64\

# Verify structure:
dir runtimes
```

**Expected output:**

```
    Directory: C:\Users\Sonal\Workspace\CashewInventoryManagementApp\installer\runtimes

Mode                 Name
----                 ----
d-----          node-v20.11.0-win-x64
d-----          nssm-2.24-101-g897c7ad
d-----          python-3.11.5-embed-amd64
```

### 2. Prepare Frontend (~1 min)

```powershell
cd ..\frontend
npm install
npm run build
```

### 3. Build the Installer (~2 min)

```powershell
cd ..\installer
.\build.ps1
```

**Or manually via Inno Setup GUI:**

- Open Inno Setup
- File → Open → Select `CashewInventoryInstaller.iss`
- Build → Compile

**Expected output:**

```
[1/5] Checking prerequisites...
✓ All required files found
[2/5] Checking runtime bundles...
✓ Python 3.11 found
✓ Node.js found
✓ NSSM found
[3/5] Checking backend preparation...
✓ Backend requirements.txt found
✓ Backend app found
[4/5] Checking frontend build...
✓ Frontend dist build found (prebuilt)
[5/5] Compiling installer...
✓ Installer compiled successfully!
  Output: C:\Users\Sonal\Workspace\CashewInventoryManagementApp\installer\Output\CashewInventorySetup.exe
  Size: 125.45 MB
```

## Testing the Installer

### 1. Run the Installer

```powershell
# Open file explorer and navigate to:
C:\Users\Sonal\Workspace\CashewInventoryManagementApp\installer\Output

# Right-click CashewInventorySetup.exe → Run as Administrator
```

### 2. Follow the Setup Wizard

- **Language**: English (OK)
- **Welcome**: Next
- **License**: Accept
- **Select Destination**: Keep default `C:\Program Files\CashewInventory` → Next
- **Select Components**: Keep all checked (App, Python, Node.js, NSSM, Shortcuts) → Next
- **Select Start Menu**: Keep default → Next
- **Select Additional Tasks**: (none) → Next
- **Ready to Install**: Install

### 3. Verify Installation

The installer will:

1. Extract files
2. Install Windows services (backend + frontend)
3. Start services automatically
4. Create desktop shortcut
5. Open browser to http://localhost:5173

**Expected behavior:**

- Cashew Inventory application opens in browser
- No console windows appear
- Desktop has "Cashew Inventory" shortcut

### 4. Check Services

Open Services Manager:

```powershell
services.msc
```

**Look for:**

- `CashewInventoryBackend` → Running
- `CashewInventoryFrontend` → Running

### 5. Review Logs

```powershell
# View log files:
explorer "C:\Program Files\CashewInventory\logs"
```

**Check:**

- `backend.log` - Should contain Uvicorn startup message
- `frontend.log` - Should contain Vite preview startup message
- `*_error.log` - Should be empty (or only contain warnings)

### 6. Test Start/Stop

**Stop the app:**

- Click "Stop Application" from Start Menu
- OR: Open Services → Stop both services

**Verify:**

```powershell
nssm status CashewInventoryBackend
nssm status CashewInventoryFrontend
```

**Start the app:**

- Click "Cashew Inventory" desktop shortcut
- OR: Open Services → Start both services

### 7. Uninstall (Optional)

Control Panel → Programs → Programs and Features → "Cashew Inventory Management" → Uninstall

## Troubleshooting

| Issue                              | Solution                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------ |
| Services fail to start             | Check `logs\backend_error.log` and `logs\frontend_error.log` for details |
| Browser doesn't open               | Manually navigate to http://localhost:5173                               |
| "Permission denied" during install | Run installer as Administrator                                           |
| Runtimes not found                 | Verify `runtimes\` subdirectories exist with files inside                |
| NSSM command not found             | Ensure `runtimes\nssm-2.24-101-g897c7ad\win64\nssm.exe` exists           |

## Next Steps

- **Distribute**: Share `CashewInventorySetup.exe` with end users
- **Customize**: Edit `CashewInventoryInstaller.iss` to change app name, icon, or branding
- **Automate**: Integrate build.ps1 into CI/CD pipeline

---

**Need Help?** Review the full [README.md](README.md) in this directory.
