# 🚀 Step-by-Step Guide: How to Run the App

## Prerequisites
- ✅ Python 3.13.5 (already installed)
- ✅ Node.js and npm (already installed)
- ✅ Virtual environment created (`.venv` folder exists)
- ✅ All dependencies installed

---

## Method 1: Automatic Start (Easiest) ⭐

### Step 1: Open PowerShell
1. Press `Windows + X`
2. Select **"Windows PowerShell"** or **"Terminal"**

### Step 2: Navigate to Project Directory
```powershell
cd "C:\Users\U S E R\OneDrive\Desktop\funai\roast-my-profile"
```

### Step 3: Run the App
```powershell
.\run_app.ps1
```

### Step 4: What Happens?
- Two new PowerShell windows will open automatically:
  - **Window 1**: Backend server (port 8000)
  - **Window 2**: Frontend server (port 3000)

### Step 5: Access the App
Open your browser and go to:
```
http://localhost:3000
```

### Step 6: Stop the App
- Press `Ctrl + C` in each PowerShell window
- Or simply close both windows

---

## Method 2: Manual Start (More Control)

### For Backend:

#### Step 1: Open PowerShell Terminal #1
```powershell
cd "C:\Users\U S E R\OneDrive\Desktop\funai\roast-my-profile"
```

#### Step 2: Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear at the start of your prompt.

#### Step 3: Navigate to Backend
```powershell
cd backend
```

#### Step 4: Start Backend Server
```powershell
python -m app.main
```

You should see:
```
🚀 Starting Roast My Profile API
✅ Configuration validated (Provider: gemini)
🔥 Roast worker started
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this window open!**

---

### For Frontend:

#### Step 5: Open PowerShell Terminal #2 (New Window)
```powershell
cd "C:\Users\U S E R\OneDrive\Desktop\funai\roast-my-profile"
```

#### Step 6: Navigate to Frontend
```powershell
cd frontend
```

#### Step 7: Start Frontend Server
```powershell
npm run dev
```

You should see:
```
VITE v7.2.4  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.x.x:3000/
```

**Keep this window open too!**

---

## 🌐 Accessing the Application

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web interface |
| **Backend API** | http://localhost:8000 | API server |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |

---

## 🛑 Stopping the Application

### Method 1 (Automatic):
- Close both PowerShell windows that opened

### Method 2 (Manual):
- In each terminal window, press `Ctrl + C`
- Wait for the server to shut down
- Type `exit` to close the terminal

---

## 🔧 Troubleshooting

### Problem: "Execution Policy" Error

If you see an error about execution policy when running `.ps1` files:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running the script again.

### Problem: Port Already in Use

If you see "Address already in use" error:

**Option 1**: Stop the other application using that port

**Option 2**: Change the port in configuration files:
- Backend: Edit `backend/app/config.py` → Change `PORT = 8000`
- Frontend: Edit `frontend/vite.config.js` → Change port in server config

### Problem: Virtual Environment Won't Activate

Make sure you're in the project root directory:
```powershell
cd "C:\Users\U S E R\OneDrive\Desktop\funai\roast-my-profile"
```

Then try:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Problem: Dependencies Missing

Re-run the setup:
```powershell
.\setup_dev.ps1
```

---

## 📝 Quick Reference Commands

### Check if servers are running:
```powershell
# Check backend
curl http://localhost:8000

# Check frontend
curl http://localhost:3000
```

### View installed Python packages:
```powershell
.\.venv\Scripts\python.exe -m pip list
```

### View installed npm packages:
```powershell
cd frontend
npm list --depth=0
```

---

## 🎯 Next Steps

1. ✅ Start the application using Method 1 or Method 2
2. ✅ Open http://localhost:3000 in your browser
3. ✅ Upload a profile picture
4. ✅ Get roasted by AI! 🔥

---

**Need help?** Check the main README.md for more information.
