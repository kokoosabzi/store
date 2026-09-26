@echo off
setlocal
title Local Commerce Core - Local Launcher
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  if errorlevel 1 (echo Python is required.& pause& exit /b 1)
)

call ".venv\Scripts\activate.bat"
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (pause& exit /b 1)

if not exist "data" mkdir data
if not exist "backups" mkdir backups
set "LCC_DATABASE_URL=sqlite:///./data/local_commerce.db"

echo Applying database migrations...
alembic upgrade head
if errorlevel 1 (pause& exit /b 1)

echo Starting FastAPI backend...
start "Local Commerce Core API" cmd /k "cd /d ""%~dp0"" && call .venv\Scripts\activate.bat && python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

if exist "frontend\package.json" (
  echo Installing/starting Vue frontend...
  cd /d "%~dp0frontend"
  if not exist "node_modules" npm install
  start "Local Commerce Core UI" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"
) else (
  echo Frontend directory not found.
)

echo Backend: http://127.0.0.1:8000/api/health
echo Frontend: check the Vite URL in the UI terminal.
pause
endlocal