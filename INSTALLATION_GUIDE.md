# 📦 Installation Guide - Garagefy

## ⚠️ Prerequisites Required

Your system is missing:
- ❌ Python (not in PATH)
- ❌ Node.js/npm (not in PATH)

You need to install these first.

---

## 🔧 Installation Steps

### Step 1: Install Python

#### Option A: Microsoft Store (Easiest)
1. Open Microsoft Store
2. Search for "Python"
3. Click "Get" to install
4. After installation, restart your terminal

#### Option B: Python.org
1. Go to https://python.org/downloads
2. Download Python 3.11 or later
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Restart your terminal

#### Verify Installation
```bash
python --version
# Should output: Python 3.x.x
```

---

### Step 2: Install Node.js

1. Go to https://nodejs.org
2. Download LTS version (recommended)
3. Run the installer
4. Accept all defaults
5. Restart your terminal

#### Verify Installation
```bash
node --version
npm --version
# Should output version numbers
```

---

## 📥 Install Garagefy Dependencies

Once Python and Node.js are installed:

### Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Expected output**: "Successfully installed X packages"

### Frontend Dependencies
```bash
cd frontend
npm install
```

**Expected output**: "added X packages"

---

## 🚀 Run Garagefy

### Terminal 1: Start Backend
```bash
cd backend
python run.py
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8099
INFO:     Application startup complete
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```

**Expected output**:
```
Compiled successfully!
You can now view garagefy in the browser.
Local: http://localhost:3000
```

### Open in Browser
```
http://localhost:3000
```

---

## ✅ Verification

### Test Backend
```bash
curl http://localhost:8099/api/fix-it/test-garages
```

### Test Baserow
```bash
cd backend
python test_baserow.py
```

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python from https://python.org
- **IMPORTANT**: Check "Add Python to PATH"
- Restart terminal after installation

### "npm not found"
- Install Node.js from https://nodejs.org
- Restart terminal after installation

### "pip: command not found"
- Use: `python -m pip install -r requirements.txt`
- Or reinstall Python with PATH option

### "npm ERR!"
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again

### "Port 8099 already in use"
- Change port in `backend/run.py`
- Or kill the process using that port

---

## 📋 Installation Checklist

- [ ] Python installed and in PATH
- [ ] Node.js installed and in PATH
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:3000
- [ ] API responds at http://localhost:8099/api/fix-it/test-garages

---

## 🎯 Next Steps

1. Install Python and Node.js
2. Run `pip install -r requirements.txt` in backend folder
3. Run `npm install` in frontend folder
4. Start backend: `python run.py`
5. Start frontend: `npm start`
6. Open http://localhost:3000

---

## 📞 Support

If you encounter issues:

1. **Check Python**: `python --version`
2. **Check Node.js**: `node --version`
3. **Check npm**: `npm --version`
4. **Reinstall**: Delete node_modules and package-lock.json, then `npm install` again
5. **Check logs**: Look for error messages in terminal

---

## ⏱️ Installation Time

- Python: 5-10 minutes
- Node.js: 5-10 minutes
- Backend deps: 5-10 minutes
- Frontend deps: 10-15 minutes
- **Total**: ~30-45 minutes

---

## 🎉 Ready to Go!

Once installed, you can:
- ✅ Run Garagefy locally
- ✅ Test the application
- ✅ Deploy to production
- ✅ Develop new features

