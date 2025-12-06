# 🚀 Running from Terminal

This guide shows you how to run the **Roast My Profile** app from your terminal.

## ✅ Setup Complete

Your virtual environment (`.venv`) has been created and all dependencies are installed!

## 🎯 Quick Start

### Option 1: Use the Run Script (Recommended)

Simply run this command in PowerShell:

```powershell
.\run_app.ps1
```

This will open **two new PowerShell windows**:
- One for the **Backend** (running on port 8000)
- One for the **Frontend** (running on port 3000)

### Option 2: Manual Start

If you prefer to run them manually in separate terminals:

**Terminal 1 - Backend:**
```powershell
.\.venv\Scripts\Activate.ps1
cd backend
python -m app.main
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

## 🌐 Access the App

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🛑 Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers.

## 🔧 Troubleshooting

### Virtual Environment Not Activating?

If `.\run_app.ps1` fails, you may need to allow script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use?

If port 8000 or 3000 is already in use, stop other applications using those ports or modify the port settings in:
- Backend: `backend/app/config.py` (PORT variable)
- Frontend: `frontend/vite.config.js`

### Missing Dependencies?

Re-run the setup script:

```powershell
.\setup_dev.ps1
```

## 📝 Notes

- The `.venv` folder contains your Python virtual environment
- Always activate the virtual environment before running backend commands
- Frontend dependencies are in `frontend/node_modules`
