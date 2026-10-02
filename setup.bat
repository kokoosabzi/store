@echo off
setlocal
title Local Commerce Core - Setup

cd /d "%~dp0"

echo ==========================================
echo   LOCAL COMMERCE CORE - SETUP
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/5] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [1/5] Python virtual environment already exists.
)

echo.
echo [2/5] Upgrading pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

echo.
echo [3/5] Installing Python dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Python dependency installation failed.
    pause
    exit /b 1
)

echo.
echo [4/5] Preparing database directories...
if not exist "data" mkdir "data"
if not exist "backups" mkdir "backups"

echo.
echo [5/5] Running database migrations...
set "PYTHONPATH=%CD%"
".venv\Scripts\python.exe" -m alembic upgrade head
if errorlevel 1 (
    echo.
    echo ERROR: Database migration failed.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Installing Frontend dependencies...
echo ==========================================
cd /d "%~dp0frontend"

if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Frontend installation failed.
        pause
        exit /b 1
    )
) else (
    echo node_modules already exists. Skipping npm install.
)

echo.
echo ==========================================
echo   SETUP COMPLETED SUCCESSFULLY
echo ==========================================
echo.
pause
endlocal