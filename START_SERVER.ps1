# Smart Plant Disease Detection System - PowerShell Startup Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Plant Disease Detection System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.14+ and add it to PATH"
    Read-Host "Press Enter to exit"
    exit 1
}

# Navigate to project directory
$projectPath = "C:\Users\srini\OneDrive\Desktop\PLANT"
Set-Location -Path $projectPath
Write-Host "[INFO] Working directory: $projectPath" -ForegroundColor Yellow

# Check and activate virtual environment
Write-Host ""
Write-Host "[INFO] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
    Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Virtual environment not found - using system Python" -ForegroundColor Yellow
}

# Check Flask installation
Write-Host ""
Write-Host "[INFO] Checking Flask installation..." -ForegroundColor Yellow
try {
    python -c "import flask; print(f'Flask version: {flask.__version__}')" | Out-Null
    Write-Host "[OK] Flask is installed and ready" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Flask not installed" -ForegroundColor Red
    Write-Host "Run: pip install -r backend/requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check model files
Write-Host ""
Write-Host "[INFO] Checking model files..." -ForegroundColor Yellow
if ((Test-Path "backend/model.pkl") -and (Test-Path "backend/model.json")) {
    Write-Host "[OK] Model files found" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Model files not found" -ForegroundColor Yellow
    Write-Host "       Run: python ml/train.py --data_dir data/sample_dataset" -ForegroundColor Yellow
}

# Check dataset
Write-Host ""
Write-Host "[INFO] Checking training dataset..." -ForegroundColor Yellow
$datasetPath = "data/sample_dataset"
if (Test-Path $datasetPath) {
    $imageCount = (Get-ChildItem "$datasetPath" -Filter "*.jpg" -Recurse).Count
    Write-Host "[OK] Dataset found ($imageCount images)" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Dataset not found" -ForegroundColor Yellow
    Write-Host "       Run: python ml/generate_sample_data.py" -ForegroundColor Yellow
}

# Start Flask server
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[INFO] Starting Flask Development Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend:  http://localhost:5000" -ForegroundColor Green
Write-Host "API Base:  http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Yellow
Write-Host "  GET  /                  - Frontend UI" -ForegroundColor White
Write-Host "  POST /predict           - Image upload for disease detection" -ForegroundColor White
Write-Host "  POST /recommendation    - Get treatment for disease" -ForegroundColor White
Write-Host "  POST /translate         - Translate text" -ForegroundColor White
Write-Host "  POST /speak             - Text-to-speech" -ForegroundColor White
Write-Host ""
Write-Host "Debug Mode: Enabled (auto-reload on code changes)" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start server
python -m flask --app backend.app run --debug

# Cleanup on exit
Write-Host ""
Write-Host "[INFO] Server stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"
