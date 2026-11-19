@echo off
chcp 65001 >nul
setlocal EnableExtensions
title Local Commerce Core - Setup
cd /d "%~dp0"
set "ROOT=%~dp0"
set "PYTHONUTF8=1"

if not defined LOCALAPPDATA (
  echo ERROR: LOCALAPPDATA is not available.
  goto :fail
)
if not defined LCC_DATA_DIR set "LCC_DATA_DIR=%LOCALAPPDATA%\LocalCommerceCore\data"
if not defined LCC_BACKUP_DIR set "LCC_BACKUP_DIR=%LOCALAPPDATA%\LocalCommerceCore\backups"
if not defined LCC_RUN_DIR set "LCC_RUN_DIR=%LOCALAPPDATA%\LocalCommerceCore\run"
if not defined LCC_LOG_DIR set "LCC_LOG_DIR=%LOCALAPPDATA%\LocalCommerceCore\logs"

if exist "%ROOT%data\local_commerce.db" if /I not "%LCC_DATA_DIR%\local_commerce.db"=="%ROOT%data\local_commerce.db" (
  echo ERROR: A repository-local data\local_commerce.db already exists.
  echo Setup will not silently switch to a new empty database or move existing data.
  echo Set LCC_DATA_DIR to the folder containing that existing database and rerun setup.bat.
  goto :fail
)

if not exist "%LCC_DATA_DIR%" mkdir "%LCC_DATA_DIR%"
if not exist "%LCC_BACKUP_DIR%" mkdir "%LCC_BACKUP_DIR%"
if not exist "%LCC_RUN_DIR%" mkdir "%LCC_RUN_DIR%"
if not exist "%LCC_LOG_DIR%" mkdir "%LCC_LOG_DIR%"

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python Launcher was not found. Install Python 3.12 and enable py.exe.
  goto :fail
)
py -3.12 --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python 3.12 was not found.
  goto :fail
)

if not exist "%ROOT%.venv\Scripts\python.exe" (
  echo [1/5] Creating Python 3.12 virtual environment...
  py -3.12 -m venv "%ROOT%.venv"
  if errorlevel 1 goto :fail
) else (
  echo [1/5] Existing virtual environment found.
)
set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"
"%PYTHON_EXE%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)"
if errorlevel 1 (
  echo ERROR: The existing .venv requires Python 3.12 or newer. Recreate .venv with Python 3.12.
  goto :fail
)

echo [2/5] Installing Python dependencies...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 goto :fail
"%PYTHON_EXE%" -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [3/5] Installing and building the Vue frontend...
where node >nul 2>&1
if errorlevel 1 (
  echo ERROR: Node.js is required only during setup to build the frontend.
  goto :fail
)
where npm >nul 2>&1
if errorlevel 1 (
  echo ERROR: npm was not found.
  goto :fail
)
cd /d "%ROOT%frontend"
call npm install
if errorlevel 1 goto :fail
call npm run build
if errorlevel 1 goto :fail
if not exist "%ROOT%frontend\dist\index.html" (
  echo ERROR: Production frontend build was not created.
  goto :fail
)

echo [4/5] Preparing local application data...
cd /d "%ROOT%"
set "PYTHONPATH=%ROOT%"
"%PYTHON_EXE%" -m alembic upgrade head
if errorlevel 1 goto :fail

echo [5/5] Verifying installation...
"%PYTHON_EXE%" -c "from backend.app.config import settings; from pathlib import Path; assert Path(settings.database_url.split('///',1)[1]).parent.exists()"
if errorlevel 1 goto :fail

echo.
echo ==========================================
echo   SETUP COMPLETED SUCCESSFULLY
echo ==========================================
echo Data: %LCC_DATA_DIR%
echo Backups: %LCC_BACKUP_DIR%
echo Run start.bat to launch the application.
if not "%LCC_NO_PAUSE%"=="1" pause
exit /b 0

:fail
echo.
echo ERROR: Setup did not complete. Existing data was not intentionally deleted or moved.
if not "%LCC_NO_PAUSE%"=="1" pause
exit /b 1
