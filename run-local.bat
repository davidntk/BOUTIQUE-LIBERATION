@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo       BOUTIQUE LIBERATION - LOCAL
echo ==========================================

where py >nul 2>nul
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe ou absent du PATH.
    echo Installe Python 3 depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [1/4] Creation de l'environnement Python...
    py -3 -m venv venv
    if errorlevel 1 goto :error
)

echo [2/4] Activation de l'environnement...
call "venv\Scripts\activate.bat"

echo [3/4] Installation des dependances...
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

if not exist "data" mkdir data
set "FLASK_HOST=0.0.0.0"
set "FLASK_PORT=5001"
set "FLASK_DEBUG=0"
if not defined SECRET_KEY set "SECRET_KEY=local-development-change-this-secret"
if not defined DB_PATH set "DB_PATH=%CD%\data\boutique_liberation.db"

echo [4/4] Demarrage du serveur...
echo.
echo Boutique : http://127.0.0.1:5001
echo Admin    : http://127.0.0.1:5001/admin
echo Sante    : http://127.0.0.1:5001/health
echo Pour arreter : CTRL+C
echo.
python app.py
goto :end

:error
echo.
echo Une erreur est survenue pendant l'installation ou le demarrage.
pause
exit /b 1

:end
endlocal
