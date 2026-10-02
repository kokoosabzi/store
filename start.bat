@echo off
setlocal

title Local Commerce Core - Start

cd /d "%~dp0"

echo ==========================================
echo   LOCAL COMMERCE CORE
echo   STARTING PROJECT
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "data" mkdir "data"
if not exist "backups" mkdir "backups"

echo [1/3] Checking database migrations...
echo.

set "PYTHONPATH=%CD%"

".venv\Scripts\python.exe" -m alembic upgrade head

if errorlevel 1 (
    echo.
    echo ERROR: Database migration failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Backend...
echo.

start "LCC Backend" cmd /k "cd /d "%~dp0" & set PYTHONPATH=%~dp0 & .venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Frontend...
echo.

start "LCC Frontend" cmd /k "cd /d "%~dp0frontend" & npm run dev"

echo.
echo ==========================================
echo   PROJECT STARTED
echo ==========================================
echo.
echo Frontend:
echo http://localhost:5173/
echo.
echo Backend:
echo http://127.0.0.1:8000/
echo.
echo API Docs:
echo http://127.0.0.1:8000/docs
echo.
echo ==========================================
echo.

timeout /t 3 /nobreak >nul

start "" "http://localhost:5173/"

endlocal