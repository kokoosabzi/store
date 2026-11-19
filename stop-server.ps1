param(
    [Parameter(Mandatory = $true)]
    [string]$PidFile
)

if (-not (Test-Path -LiteralPath $PidFile)) {
    Write-Output "Local Commerce Core is not running (no PID file)."
    exit 0
}

$raw = Get-Content -LiteralPath $PidFile -Raw -ErrorAction SilentlyContinue
[int]$serverProcessId = 0
if ([string]::IsNullOrWhiteSpace($raw) -or -not [int]::TryParse($raw.Trim(), [ref]$serverProcessId)) {
    Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
    Write-Output "Removed an invalid stale PID file."
    exit 0
}

$process = Get-CimInstance Win32_Process -Filter "ProcessId=$serverProcessId" -ErrorAction SilentlyContinue
if ($process -and $process.CommandLine -match "uvicorn backend.app.main:app") {
    Stop-Process -Id $serverProcessId -Force -ErrorAction Stop
    Start-Sleep -Milliseconds 500
    if (Get-Process -Id $serverProcessId -ErrorAction SilentlyContinue) {
        throw "Local Commerce Core server process $serverProcessId did not stop."
    }
}

Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
Write-Output "Local Commerce Core stopped."
exit 0
