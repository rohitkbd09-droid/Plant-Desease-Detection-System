@echo off
REM Smart Plant Disease Detection System - Startup Script
REM Windows Command Prompt Version

echo.
echo ========================================
echo Plant Disease Detection System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.14+ and add it to PATH
    pause
    exit /b 1
)

REM Navigate to project directory
cd /d "C:\Users\srini\OneDrive\Desktop\PLANT"

echo [INFO] Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [WARNING] Virtual environment not found
    echo [INFO] Using system Python
)

echo.
echo [INFO] Checking Flask installation...
python -c "import flask; print('[OK] Flask version:', flask.__version__)" || (
    echo [ERROR] Flask not installed. Run: pip install -r backend/requirements.txt
    pause
    exit /b 1
)

echo.
echo [INFO] Starting Flask development server...
echo [INFO] Server will be available at: http://localhost:5000
echo [INFO] Frontend URL: http://localhost:5000
echo [INFO] API Base URL: http://localhost:5000/api
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.

python -m flask --app backend.app run --debug

pause
