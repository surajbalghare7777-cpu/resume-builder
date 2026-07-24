# Setup Guide 🛠️

This guide will help you set up your development environment and get the Resume Builder app running on your machine.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing Python](#installing-python)
3. [Setting Up the Project](#setting-up-the-project)
4. [Installing Dependencies](#installing-dependencies)
5. [Running the Application](#running-the-application)
6. [Verifying the Setup](#verifying-the-setup)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free space
- **Internet**: Required for initial setup

### Software Requirements

- **Python**: Version 3.8 or higher
- **Web Browser**: Chrome 90+, Firefox 88+, Edge 90+, or Safari 14+
- **Text Editor**: VS Code, Sublime Text, Atom, or any code editor

---

## Installing Python

### Windows

1. **Download Python**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.11 or latest version
   - Run the installer

2. **Installation Steps**
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**

   ```bash
   python --version
   # Should output: Python 3.x.x

   pip --version
   # Should output: pip 23.x.x
   ```

### macOS

1. **Using Homebrew** (Recommended)

   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python
   brew install python@3.11
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

---

## Setting Up the Project

### Step 1: Create Project Directory

```bash
# Navigate to your desired location
cd Desktop

# Create project folder
mkdir resume-builder
cd resume-builder
```

### Step 2: Create Folder Structure

Create the following folders:

```bash
# On Windows (PowerShell)
New-Item -ItemType Directory -Path static\css, static\js, templates, docs

# On macOS/Linux
mkdir -p static/css static/js templates docs
```

Your structure should look like:

```
resume-builder/
├── docs/
├── static/
│   ├── css/
│   └── js/
└── templates/
```

---

## Installing Dependencies

### Step 1: Create requirements.txt

Create a file named `requirements.txt` in the project root with the following content:

```txt
Flask==3.0.0
Flask-CORS==4.0.0
reportlab==4.0.7
Pillow==10.1.0
```

### Step 2: Create Virtual Environment (Recommended)

**Why use a virtual environment?**

- Isolates project dependencies
- Prevents conflicts with other Python projects
- Easy to manage and reproduce

**Windows:**

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**macOS/Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Expected Output:**

```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 reportlab-4.0.7 Pillow-10.1.0 ...
```

### Step 4: Verify Installation

```bash
pip list
```

You should see Flask, Flask-CORS, reportlab, and Pillow in the list.

---

## Running the Application

### Step 1: Start the Flask Server

```bash
# Make sure you're in the project directory
# and virtual environment is activated

python app.py
```

**Expected Output:**

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 2: Open in Browser

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the Resume Builder interface

---

## Verifying the Setup

### Checklist ✅

- [ ] Python 3.8+ installed and accessible
- [ ] Project folder structure created
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Flask server starts without errors
- [ ] Application loads in browser
- [ ] No console errors in browser DevTools

### Testing Basic Functionality

1. **Test Form Input**
   - Enter your name in the form
   - Check if it appears in the preview section

2. **Test Browser Console**
   - Press `F12` to open DevTools
   - Check Console tab for errors
   - Should see no red error messages

3. **Test Server Response**
   - Check terminal where Flask is running
   - Should see GET requests logged

---

## Common Setup Issues

### Issue: "Python not found"

**Solution:**

- Reinstall Python with "Add to PATH" checked
- Or manually add Python to system PATH

### Issue: "pip not found"

**Solution:**

```bash
python -m ensurepip --upgrade
```

### Issue: "Permission denied" on Linux/macOS

**Solution:**

```bash
# Use pip with --user flag
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:**

```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

---

## Next Steps

✅ **Setup Complete!**

Now you're ready to start building. Proceed to:

- **[Architecture Guide](02-ARCHITECTURE.md)** - Understand the system design
- **[Building Frontend](03-BUILDING-FRONTEND.md)** - Start coding the interface

---

## Quick Reference Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Deactivate virtual environment
deactivate
```

---

**Need help?** Check the [Troubleshooting Guide](06-TROUBLESHOOTING.md) or review the error messages carefully.
