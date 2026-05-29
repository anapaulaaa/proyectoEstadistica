@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo No se encontro el entorno .venv\Scripts\python.exe
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" -m PyInstaller main.py --name StatPro --windowed --noconfirm --clean --onefile --add-data "datos;datos" --add-data "assets;assets"

echo.
echo Build terminado. Revisa la carpeta dist\ para encontrar StatPro.exe.
endlocal