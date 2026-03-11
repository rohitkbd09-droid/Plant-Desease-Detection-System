@echo off
cd /d "C:\Users\srini\OneDrive\Desktop\PLANT"
call .venv\Scripts\activate.bat
python -m flask --app backend.app run --debug --host=0.0.0.0 --port=5000
pause
