Set objShell = CreateObject("WScript.Shell")
strPath = "C:\Users\srini\OneDrive\Desktop\PLANT"
objShell.CurrentDirectory = strPath
objShell.Run "cmd.exe /c cd /d " & strPath & " && call .venv\Scripts\activate.bat && python -m flask --app backend.app run --debug --host=0.0.0.0 --port=5000", 0, False
WScript.Sleep 2000
objShell.Run "http://localhost:5000", 1
