@echo off
setlocal EnableExtensions
if not defined LOCALAPPDATA exit /b 1
if not defined LCC_RUN_DIR set "LCC_RUN_DIR=%LOCALAPPDATA%\LocalCommerceCore\run"
set "PID_FILE=%LCC_RUN_DIR%\server.pid"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop-server.ps1" -PidFile "%PID_FILE%"
if errorlevel 1 (
  echo ERROR: Could not stop Local Commerce Core.
  exit /b 1
)
exit /b 0
