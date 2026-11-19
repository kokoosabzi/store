@echo off
chcp 65001 >nul
setlocal EnableExtensions
title Local Commerce Core - Start
cd /d "%~dp0"
set "ROOT=%~dp0"
set "PYTHONUTF8=1"

if not defined LOCALAPPDATA (
  echo ERROR: LOCALAPPDATA is not available.
  exit /b 1
)
if not defined LCC_DATA_DIR set "LCC_DATA_DIR=%LOCALAPPDATA%\LocalCommerceCore\data"
if not defined LCC_BACKUP_DIR set "LCC_BACKUP_DIR=%LOCALAPPDATA%\LocalCommerceCore\backups"
if not defined LCC_RUN_DIR set "LCC_RUN_DIR=%LOCALAPPDATA%\LocalCommerceCore\run"
if not defined LCC_LOG_DIR set "LCC_LOG_DIR=%LOCALAPPDATA%\LocalCommerceCore\logs"
set "PID_FILE=%LCC_RUN_DIR%\server.pid"
set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
  echo ERROR: Virtual environment not found. Run setup.bat first.
  exit /b 1
)
if not exist "%ROOT%frontend\dist\index.html" (
  echo ERROR: Production frontend is missing. Run setup.bat first.
  exit /b 1
)
if not exist "%LCC_DATA_DIR%" mkdir "%LCC_DATA_DIR%"
if not exist "%LCC_BACKUP_DIR%" mkdir "%LCC_BACKUP_DIR%"
if not exist "%LCC_RUN_DIR%" mkdir "%LCC_RUN_DIR%"
if not exist "%LCC_LOG_DIR%" mkdir "%LCC_LOG_DIR%"

set "PYTHONPATH=%ROOT%"
"%PYTHON_EXE%" -m alembic upgrade head
if errorlevel 1 (
  echo ERROR: Database migration failed. The application was not started.
  exit /b 1
)

for /f "delims=" %%P in ('powershell -NoProfile -Command "if (Test-Path '%PID_FILE%') { $serverProcessId = (Get-Content '%PID_FILE%' -Raw).Trim(); $p = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $serverProcessId) -ErrorAction SilentlyContinue; if ($p -and $p.CommandLine -match 'uvicorn backend.app.main:app') { Write-Output 'RUNNING' } else { Remove-Item '%PID_FILE%' -Force -ErrorAction SilentlyContinue } }"') do set "SERVER_STATE=%%P"
if /I "%SERVER_STATE%"=="RUNNING" (
  echo Local Commerce Core is already running at http://127.0.0.1:8000/
  if not "%LCC_NO_BROWSER%"=="1" start "" "http://127.0.0.1:8000/"
  exit /b 0
)

echo Starting Local Commerce Core...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p = Start-Process -FilePath '%PYTHON_EXE%' -ArgumentList @('-m','uvicorn','backend.app.main:app','--host','127.0.0.1','--port','8000') -WorkingDirectory '%ROOT%' -WindowStyle Hidden -RedirectStandardOutput '%LCC_LOG_DIR%\server.log' -RedirectStandardError '%LCC_LOG_DIR%\server-error.log' -PassThru; Set-Content -Path '%PID_FILE%' -Value $p.Id"
if errorlevel 1 (
  echo ERROR: Could not launch the backend. Check %LCC_LOG_DIR%\server-error.log
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready = $false; for ($i = 0; $i -lt 20; $i++) { try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1; if ($r.StatusCode -eq 200) { $ready = $true; break } } catch { }; Start-Sleep -Milliseconds 500 }; if ($ready) { if ($env:LCC_NO_BROWSER -ne '1') { Start-Process 'http://127.0.0.1:8000/' }; exit 0 }; exit 1"
if errorlevel 1 (
  echo ERROR: The application did not become healthy. Check %LCC_LOG_DIR%\server-error.log
  call "%ROOT%stop.bat"
  exit /b 1
)

echo Local Commerce Core is ready at http://127.0.0.1:8000/
echo Logs: %LCC_LOG_DIR%
exit /b 0
