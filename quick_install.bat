@echo off
echo 🤖 Steve Voice Assistant - Quick Install Script
echo ===============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Create virtual environment (optional)
set /p USE_VENV="Create virtual environment? (y/n): "
if /i "%USE_VENV%"=="y" (
    echo 📦 Creating virtual environment...
    python -m venv steve_env
    call steve_env\Scripts\activate.bat
    echo ✅ Virtual environment activated
)

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run setup script
echo 🔧 Running setup...
python setup.py

if %errorlevel% neq 0 (
    echo ⚠️ Setup completed with warnings
) else (
    echo ✅ Setup completed successfully!
)

echo.
echo 🎉 Installation complete!
echo.
echo Next steps:
echo 1. Add your Google AI API key to .env file
echo 2. Run: python steve_voice_assistant.py
echo 3. Say "Hey Steve" to start chatting!
echo.

if /i "%USE_VENV%"=="y" (
    echo 📝 Note: To activate the virtual environment later, run:
    echo    steve_env\Scripts\activate.bat
    echo.
)

pause