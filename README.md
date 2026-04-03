# Cashew Inventory Management

Cashew Inventory Management is a desktop-based application designed to manage inventory operations with a Python backend and a React-based frontend. The application is packaged with a Windows installer for easy deployment.

---

## 🚀 Overview

This project consists of:

- **Frontend**: React application (served as static build)
- **Backend**: Python-based API/service
- **Database**: SQL scripts for schema and data
- **Installer**: Windows installer built using Inno Setup

---

## 🧩 Project Structure

```
.
├── frontend/          # React application
├── backend/           # Python backend
├── database/          # SQL scripts
├── installer/         # Installer scripts and configuration
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

- Frontend is built into static files (`dist/`)
- Backend runs using Python
- Installer packages everything into a Windows executable
- Application is launched using a script-based launcher (no console UI)

---

## 🛠️ Development Setup

### 1. Frontend

```
cd frontend
npm install
npm run build
```

---

### 2. Backend

```
cd backend
pip install -r requirements.txt
python app.py
```

---

### 3. Database

- SQL scripts are available in the `database/` folder
- Run manually or integrate with backend setup

---

## 📦 Installer

The project includes two installers:

### 🟢 Full Installer

- For first-time setup
- Includes embedded Python runtime
- Does not require pre-installed dependencies

### 🔵 Update Installer

- For existing users
- Updates application files only
- Includes backup and rollback mechanism

---

## 🏗️ Building the Installer

### Prerequisites

- Inno Setup installed
- Frontend build completed (`frontend/dist`)
- Python runtime placed locally (not in Git)

---

### Build Steps

```
cd frontend
npm run build
```

Then compile using Inno Setup:

- `installer/CashewInventory_Full.iss`
- `installer/CashewInventory_Update.iss`

---

## ⚠️ Important Notes

- Runtime files (Python) are **not stored in Git**
- Installer expects runtime to be present locally during build
- Node.js is **not required at runtime**

---

## 📁 Logs

Logs are stored at:

```
C:\ProgramData\CashewInventory\logs
```

---

## 🔄 Update Safety

The update installer includes:

- ✅ Automatic backup before update
- ✅ Rollback on failure
- ✅ Version checks (prevents downgrade)

---

## 🧠 Design Principles

- Keep runtime isolated (embedded Python)
- Avoid installing dependencies during setup
- Keep update process safe and reversible
- Maintain clean and lightweight Git repository

---

## 📌 Future Improvements

- Database migration support
- Versioned releases
- Automated build pipeline
- Cross-platform support

---

## 👩‍💻 Author

Cashew Inventory Team

---

## 📄 License

Internal / Private Use
