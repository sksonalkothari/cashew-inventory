# Installer Architecture Diagrams

## High-Level System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│         CASHEW INVENTORY MANAGEMENT - WINDOWS INSTALLER             │
└─────────────────────────────────────────────────────────────────────┘

                         End-User Machine (Windows)
                         ══════════════════════════
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                                     │
        ┌────────▼────────┐               ┌────────────▼────────┐
        │ Desktop Shortcut │               │  Start Menu Entry   │
        │ (Click to Start) │               │  (Show Stop Option) │
        └────────┬────────┘               └─────────────────────┘
                 │
                 ▼
        ┌─────────────────────────┐
        │  AppLauncher.vbs        │
        │  (Runs Hidden)          │
        │  - No console window    │
        │  - Shows toast notify   │
        └────────┬────────────────┘
                 │
                 ▼
        ┌─────────────────────────┐
        │  AppLauncher.bat        │
        │  - Manages services     │
        │  - Opens browser        │
        └────────┬────────────────┘
                 │
    ┌────────────┼────────────────┐
    │                             │
    ▼                             ▼
┌──────────────┐            ┌──────────────┐
│   NSSM       │            │   NSSM       │
│  Backend     │            │  Frontend    │
│ Service Mgr  │            │ Service Mgr  │
└──────┬───────┘            └──────┬───────┘
       │                           │
       ▼                           ▼
┌──────────────────────┐  ┌──────────────────────┐
│ Python 3.11          │  │ Node.js              │
│ + Uvicorn            │  │ + Vite Preview       │
│ Port: 8000           │  │ Port: 5173           │
│ Process: Background  │  │ Process: Background  │
│ Logs: backend.log    │  │ Logs: frontend.log   │
└──────────────────────┘  └──────────────────────┘
```

## Installation Flow

```
┌──────────────────────────────────────────────┐
│ CashewInventorySetup.exe                     │
│ (User clicks "Run as Administrator")         │
└──────────────┬───────────────────────────────┘
               │
               ▼
       ┌───────────────────┐
       │  Inno Setup GUI   │
       │  - Welcome        │
       │  - License        │
       │  - Destination    │
       │  - Components     │
       │  - Start Menu     │
       └────────┬──────────┘
                │
                ▼
       ┌──────────────────────┐
       │  Extract Files       │
       │  to Installation Dir │
       │  C:\Program Files\   │
       │  CashewInventory\    │
       └────────┬─────────────┘
                │
                ▼
       ┌──────────────────────┐
       │  Create logs/        │
       │  Directory with      │
       │  Permissions         │
       └────────┬─────────────┘
                │
                ▼
       ┌──────────────────────┐
       │  Run                 │
       │  install_services.   │
       │  bat                 │
       │  (Elevated)          │
       └────────┬─────────────┘
                │
    ┌───────────┼────────────┐
    │                        │
    ▼                        ▼
┌──────────────────┐  ┌──────────────────┐
│ Install Backend  │  │ Install Frontend │
│ Service via NSSM │  │ Service via NSSM │
│ - Set app dir    │  │ - npm install    │
│ - Set logs path  │  │ - npm build      │
│ - Set startup    │  │ - Set startup    │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         ▼                     ▼
    ┌──────────┐         ┌──────────┐
    │ Start    │         │ Start    │
    │ Service  │         │ Service  │
    └────┬─────┘         └────┬─────┘
         │                    │
         ▼                    ▼
    [Backend Running]    [Frontend Running]
    (No Console)         (No Console)
         │                    │
         └────────┬───────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ Open Browser to │
        │ http://localhost │
        │:5173            │
        └─────────────────┘
```

## Service Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Windows Services (services.msc)               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Service Name: CashewInventoryBackend                            │
│  ├─ Status: Running (or Stopped)                                 │
│  ├─ Startup Type: Automatic                                      │
│  ├─ Log On As: Local System                                      │
│  ├─ Path: NSSM → Python.exe → app.main:app                       │
│  ├─ Working Dir: C:\Program Files\CashewInventory\backend        │
│  ├─ Port: 8000                                                   │
│  ├─ Logs: C:\Program Files\CashewInventory\logs\                 │
│  │        ├─ backend.log (stdout)                                │
│  │        └─ backend_error.log (stderr)                          │
│  └─ Auto-restart: Yes (with 5s delay)                            │
│                                                                  │
│  Service Name: CashewInventoryFrontend                           │
│  ├─ Status: Running (or Stopped)                                 │
│  ├─ Startup Type: Automatic                                      │
│  ├─ Log On As: Local System                                      │
│  ├─ Path: NSSM → npm.cmd → run preview                           │
│  ├─ Working Dir: C:\Program Files\CashewInventory\frontend       │
│  ├─ Port: 5173                                                   │
│  ├─ Logs: C:\Program Files\CashewInventory\logs\                 │
│  │        ├─ frontend.log (stdout)                               │
│  │        └─ frontend_error.log (stderr)                         │
│  └─ Auto-restart: Yes (with 5s delay)                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Log Flow Architecture

```
┌────────────────────────────────────────────────────────────────┐
│         Application Logging & Log File Management              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Backend (Python Uvicorn)                                      │
│  ──────────────────────────                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ stdout/stderr from Python process                       │   │
│  │ (Uvicorn startup, API logs, etc.)                       │   │
│  └────────────┬───────────────────────────────────────────┘   │
│               │                                                │
│               ├─→ NSSM AppStdout                              │
│               │   └─→ C:\Program Files\CashewInventory\       │
│               │       logs\backend.log                        │
│               │                                                │
│               └─→ NSSM AppStderr                              │
│                   └─→ C:\Program Files\CashewInventory\       │
│                       logs\backend_error.log                  │
│                                                                │
│  Frontend (Node Vite Preview)                                  │
│  ──────────────────────────                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ stdout/stderr from Node process                         │   │
│  │ (Vite server startup, build logs, etc.)                 │   │
│  └────────────┬───────────────────────────────────────────┘   │
│               │                                                │
│               ├─→ NSSM AppStdout                              │
│               │   └─→ C:\Program Files\CashewInventory\       │
│               │       logs\frontend.log                       │
│               │                                                │
│               └─→ NSSM AppStderr                              │
│                   └─→ C:\Program Files\CashewInventory\       │
│                       logs\frontend_error.log                 │
│                                                                │
│  User can review logs for:                                     │
│  ├─ Service startup/shutdown events                           │
│  ├─ Application errors                                        │
│  ├─ Port binding issues                                       │
│  ├─ Database connection problems                              │
│  ├─ HTTP request logs (if configured)                         │
│  └─ Dependency import errors                                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Launcher Execution Path

```
Desktop Shortcut or Start Menu
         │
         ▼
    Target: C:\Program Files\CashewInventory\bin\AppLauncher.vbs
    Parameters: start (or stop, status)
         │
         ▼
    ┌─────────────────────────┐
    │ AppLauncher.vbs         │
    │ (VBScript)              │
    │                         │
    │ - Runs hidden           │
    │ - No console window     │
    │ - Executes AppLauncher. │
    │   bat with action param │
    │ - Waits for completion  │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ AppLauncher.bat         │
    │ (Batch Script)          │
    │                         │
    │ - Parses action param   │
    │ - Calls NSSM with cmds  │
    │ - Manages services      │
    │ - Shows notifications   │
    │ - Opens browser (start) │
    └────────┬────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
   START    STOP    STATUS
    │        │        │
    ├→ NSSM   ├→ NSSM  └→ NSSM status
    │  start  │  stop    CashewInventory
    │         │          Backend
    ├→ Wait   └→ Wait
    │                  ├→ Display results
    ├→ Open          └→ Show notifications
    │  browser
    │
    └→ Show
       notification
```

## Directory Structure Flow

```
Installation Directory: C:\Program Files\CashewInventory
├── backend/                         [User's backend code]
│   ├── app/
│   │   ├── main.py                 [FastAPI entry point]
│   │   ├── config.py               [Configuration]
│   │   ├── controllers/            [API routes]
│   │   ├── dao/                    [Database access]
│   │   ├── models/                 [Pydantic models]
│   │   └── ...                     [Other modules]
│   ├── requirements.txt            [Python dependencies]
│   └── venv/                       [Virtual env - NOT bundled]
│
├── frontend/                        [User's frontend code]
│   ├── dist/                       [Built frontend (npm run build)]
│   ├── src/                        [Frontend source]
│   ├── public/                     [Static assets]
│   ├── package.json                [NPM dependencies]
│   ├── vite.config.ts              [Vite config]
│   └── node_modules/               [NPM packages - created at install]
│
├── database/                        [Schema files]
│   ├── supabase-schema/
│   │   ├── 01_tables/
│   │   ├── 02_seed/
│   │   └── ...
│   └── [Optional - for documentation]
│
├── runtimes/                        [Bundled execution environments]
│   ├── python/                     [Python 3.11 embeddable]
│   │   ├── python.exe              [Python interpreter]
│   │   ├── pythonw.exe             [Python (windowed)]
│   │   ├── Lib/                    [Standard library]
│   │   └── ...
│   │
│   └── node/                       [Node.js portable]
│       ├── node.exe                [Node interpreter]
│       ├── npm.cmd                 [NPM wrapper]
│       ├── npx.cmd                 [NPX wrapper]
│       ├── node_modules/           [Built-in modules]
│       └── ...
│
├── logs/                           [★ AUTO-CREATED DURING INSTALL]
│   ├── backend.log                 [Backend stdout logs]
│   ├── backend_error.log           [Backend stderr logs]
│   ├── frontend.log                [Frontend stdout logs]
│   └── frontend_error.log          [Frontend stderr logs]
│
└── bin/                            [Executables & scripts]
    ├── nssm.exe                    [Service manager executable]
    ├── AppLauncher.vbs             [VBScript launcher]
    ├── AppLauncher.bat             [Batch launcher]
    ├── AppLauncher.ps1             [PowerShell launcher]
    ├── start_services.bat          [Manual start script]
    ├── stop_services.bat           [Manual stop script]
    ├── install_services.bat        [Service installer]
    └── uninstall_services.bat      [Service uninstaller]
```

## Uninstallation Flow

```
Control Panel → Programs → Uninstall
         │
         ▼
Find "Cashew Inventory Management"
         │
         ▼
    Click "Uninstall"
         │
         ▼
    [Run uninstall_services.bat] (Elevated)
         │
    ┌────┴────┐
    │          │
    ▼          ▼
NSSM stop   NSSM stop
Backend     Frontend
    │          │
    ├─→ NSSM remove CashewInventoryBackend
    │
    └─→ NSSM remove CashewInventoryFrontend
         │
         ▼
    [Inno Setup removes files]
    C:\Program Files\CashewInventory\*
    (EXCEPT logs/ directory)
         │
         ▼
    Remove shortcuts
    - Desktop shortcut
    - Start Menu entries
         │
         ▼
    Remove registry keys
         │
         ▼
    Installation Complete (Logs remain)
```

## Service Dependency Graph

```
Windows OS
    │
    ├─→ Service Manager (services.msc)
    │   │
    │   ├─→ CashewInventoryBackend (Service)
    │   │   │
    │   │   ├─→ NSSM (Service wrapper)
    │   │   │   │
    │   │   │   ├─→ Python.exe (interpreter)
    │   │   │   │   │
    │   │   │   │   └─→ Uvicorn ASGI server
    │   │   │   │       ├─→ FastAPI app
    │   │   │   │       └─→ Listen port 8000
    │   │   │   │
    │   │   │   └─→ Logs: backend.log, backend_error.log
    │   │   │
    │   │   └─→ Working Dir: ./backend
    │   │       └─→ Connection to Supabase (env vars)
    │   │
    │   └─→ CashewInventoryFrontend (Service)
    │       │
    │       ├─→ NSSM (Service wrapper)
    │       │   │
    │       │   ├─→ npm.cmd (Node package manager)
    │       │   │   │
    │       │   │   └─→ Vite Preview server
    │       │   │       ├─→ React SPA
    │       │   │       └─→ Listen port 5173
    │       │   │
    │       │   └─→ Logs: frontend.log, frontend_error.log
    │       │
    │       └─→ Working Dir: ./frontend
    │           └─→ dist/ (prebuilt frontend)
    │
    └─→ Browser (user navigates to http://localhost:5173)
        │
        ├─→ Frontend loads (port 5173)
        │   │
        │   └─→ API calls to Backend (port 8000)
        │       │
        │       ├─→ Authentication
        │       ├─→ Data operations
        │       └─→ Business logic
        │
        └─→ User interacts with app
```

---

**Diagrams Version**: 1.0  
**Last Updated**: February 2026
