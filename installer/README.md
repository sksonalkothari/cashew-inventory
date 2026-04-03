# Cashew Inventory Management - Installer Guide

This directory contains the installer scripts and configuration for building a Windows executable installer for the Cashew Inventory Management Application. The installer bundles Python, Node.js, and all application files into a single `.exe` file.

## Overview

- **Installer Type**: Inno Setup (modern, lightweight, open-source)
- **Bundled Runtimes**: Python 3.11 (embedded) + Node.js (portable)
- **Service Management**: NSSM (Non-Sucking Service Manager)
- **Console Suppression**: Services run hidden (no console windows)
- **Estimated Size**: ~120-150 MB installer, ~350-400 MB installed

## Prerequisites

### To Build the Installer

1. **Inno Setup 6.2+** - Download from [jrsoftware.org](https://jrsoftware.org/isdl.php)
2. **Runtimes** (must be downloaded separately due to size):

   - Python 3.11 embeddable: [python.org/downloads](https://www.python.org/downloads/windows/)
   - Node.js portable (Windows x64): [nodejs.org](https://nodejs.org/en/download/prebuilt-binaries)
   - NSSM 2.24+: [nssm.cc](https://nssm.cc/download)

3. **Build System**:
   - Windows 10/11
   - PowerShell 5.0+
   - 500+ MB free disk space

## Directory Structure

```
installer/
├── CashewInventoryInstaller.iss       # Main Inno Setup script
├── launcher/
│   ├── AppLauncher.bat                # Batch launcher (executes services)
│   ├── AppLauncher.vbs                # VBScript wrapper (hidden launch)
│   ├── AppLauncher.ps1                # PowerShell launcher (advanced features)
│   ├── start_services.bat             # Manual service start script
│   ├── stop_services.bat              # Manual service stop script
│   ├── install_services.bat           # Service installation script
│   └── uninstall_services.bat         # Service removal script
├── runtimes/                          # (Must be created - see below)
│   ├── python-3.11.5-embed-amd64/     # Extract Python embeddable here
│   ├── node-v20.11.0-win-x64/         # Extract Node.js portable here
│   └── nssm-2.24-101-g897c7ad/win64/  # Extract NSSM here
└── README.md                          # This file
```

## Build Instructions

### Step 1: Prepare Runtimes

1. Create the `runtimes` directory:

   ```powershell
   mkdir installer\runtimes -Force
   ```

2. **Download Python Embeddable**:

   - Go to https://www.python.org/downloads/windows/
   - Download "Windows embeddable package (64-bit)" for Python 3.11
   - Extract to `installer\runtimes\python-3.11.5-embed-amd64\`

3. **Download Node.js**:

   - Go to https://nodejs.org/en/download/prebuilt-binaries
   - Download Windows (x64) binary zip
   - Extract to `installer\runtimes\node-v20.11.0-win-x64\`

4. **Download NSSM**:
   - Go to https://nssm.cc/download
   - Download the latest stable release
   - Extract the `win64\nssm.exe` to `installer\runtimes\nssm-2.24-101-g897c7ad\win64\`

### Step 2: Prepare Python Dependencies

Before building the installer, ensure the backend's `requirements.txt` is ready:

```powershell
cd backend
python -m pip install -r requirements.txt
```

(The installer will install these via pip when services are installed.)

### Step 3: Prepare Frontend Build

Pre-build the frontend to reduce first-run time:

```powershell
cd frontend
npm install
npm run build
```

### Step 4: Compile the Installer

1. Open **Inno Setup Compiler**
2. File → Open → Select `CashewInventoryInstaller.iss`
3. Click "Build" → "Compile"
4. Installer will be created in `installer\Output\CashewInventorySetup.exe`

**OR** via PowerShell:

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Path\To\CashewInventoryInstaller.iss"
```

## Installation (End-User Instructions)

1. Run `CashewInventorySetup.exe` with **Administrator privileges**
2. Follow the setup wizard:
   - Choose installation type: "Full installation" (recommended)
   - Select components: App, Python, Node.js, NSSM, Shortcuts
   - Choose installation directory (default: `C:\Program Files\CashewInventory`)
3. Installer will:
   - Extract all files
   - Create `logs` directory
   - Install Windows services (backend + frontend)
   - Start both services automatically
   - Create desktop shortcut
4. Browser will automatically open to http://localhost:5173

## Post-Installation

### Starting/Stopping the Application

- **Start**: Click "Cashew Inventory" desktop shortcut (or Start Menu → Cashew Inventory)
- **Stop**: Click "Stop Application" in Start Menu
- **Manual**: Use services snapin (press `Win+R`, type `services.msc`, find `CashewInventoryBackend` and `CashewInventoryFrontend`)

### Logs

Application logs are stored in:

```
C:\Program Files\CashewInventory\logs\
```

Files:

- `backend.log` - Backend API logs
- `backend_error.log` - Backend errors
- `frontend.log` - Frontend server logs
- `frontend_error.log` - Frontend errors

### Manual Service Control

For advanced users, use command line:

```powershell
# Start services
& "C:\Program Files\CashewInventory\bin\start_services.bat" "C:\Program Files\CashewInventory"

# Stop services
& "C:\Program Files\CashewInventory\bin\stop_services.bat" "C:\Program Files\CashewInventory"

# Check status
nssm status CashewInventoryBackend
nssm status CashewInventoryFrontend
```

## Uninstallation

1. Go to Control Panel → Programs → Programs and Features
2. Find "Cashew Inventory Management"
3. Click "Uninstall"
4. Installer will:
   - Stop services
   - Remove services
   - Delete all application files
   - Remove shortcuts

**Note**: The `logs` directory is NOT deleted during uninstallation (for data preservation).

## Troubleshooting

### Services fail to start after install

- Verify Python and Node.js runtimes extracted correctly
- Check `logs\backend_error.log` and `logs\frontend_error.log`
- Run installer again with administrator privileges
- Manually re-install services:
  ```powershell
  & "C:\Program Files\CashewInventory\bin\install_services.bat" "C:\Program Files\CashewInventory"
  ```

### Browser doesn't open automatically

- Manually navigate to http://localhost:5173
- Check firewall rules (ports 8000 and 5173 should be open)
- Verify frontend service is running: `nssm status CashewInventoryFrontend`

### Backend connection errors

- Verify backend service is running: `nssm status CashewInventoryBackend`
- Check database connection string in `backend\app\config.py`
- Review `logs\backend_error.log` for details

### High memory or CPU usage

- Check running processes for `python.exe` and `node.exe`
- Review log files for errors in loops
- Verify database queries are optimized

### Uninstall fails

- Ensure services are stopped: `nssm stop CashewInventoryBackend` and `nssm stop CashewInventoryFrontend`
- Run uninstaller with administrator privileges
- Manual removal: Delete `C:\Program Files\CashewInventory` folder

## Advanced Customization

### Change Application Ports

Edit the relevant service command in `install_services.bat`:

- **Backend**: Change `--port 8000` to desired port
- **Frontend**: Change `vite preview --port 5173` to desired port
- Update AppLauncher launcher accordingly

### Change Service Names

Search and replace in all `.bat` and `.ps1` files:

- `CashewInventoryBackend` → your backend service name
- `CashewInventoryFrontend` → your frontend service name

### Use Different Python/Node Versions

1. Update paths in `CashewInventoryInstaller.iss` (`Source:` lines)
2. Update service command in `install_services.bat` (if executable paths differ)

### Enable Debug Logging

In `install_services.bat`, add more detail to service environment:

```batch
"%NSSM%" set "%BACKEND_SERVICE%" AppEnvironmentExtra "PYTHONUNBUFFERED=1"
```

## Distribution

### Creating a Smaller Installer

- **Omit Python/Node**: Require users to install system Python 3.11+ and Node.js 18+
  - Change installer type to "Minimal"
  - Update service commands to use system binaries
  - Reduces installer to ~30-50 MB

### Creating an Online Installer

- Host runtimes on a CDN
- Download during install (requires internet)
- Reduces offline installer to ~5-10 MB

## File Checksums (for security)

Generate and document checksums for distribution:

```powershell
Get-FileHash Output\CashewInventorySetup.exe | Format-List
```

## Support & License

For issues or feature requests, contact the development team.

---

**Installer Version**: 1.0.0  
**Last Updated**: February 2026
