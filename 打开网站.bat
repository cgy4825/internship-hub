@echo off
setlocal enabledelayedexpansion
title Start Internship Hub
echo ==============================================
echo   Starting Internship Hub ...
echo ==============================================
echo.

rem Auto-install dependencies on first run
if not exist "%~dp0web\node_modules" (
    echo [first run] Installing dependencies, please wait...
    call cmd /c "cd /d "%~dp0web" && npm install"
    if errorlevel 1 echo [warn] npm install may have had an issue, continuing...
)

echo [start] Starting dev server on port 5300 ...
rem Open a new window running npm run dev, with correct working directory
start "internship-hub - dev server" cmd /k "cd /d "%~dp0web" && npm run dev"

rem Wait for the port to be ready (up to ~25s)
set port_ready=0
for /l %%i in (1,1,25) do (
    "%SystemRoot%\System32\curl.exe" -s -o nul -w "%%{http_code}" http://localhost:5300/ > "%TEMP%\_ih_check.txt" 2>nul
    set /p code= < "%TEMP%\_ih_check.txt"
    if "!code!"=="200" (
        set port_ready=1
        goto ready
    )
    timeout /t 1 /nobreak >nul
)

:ready
if "%port_ready%"=="1" (
    echo.
    echo [OK] Server is ready, opening browser...
    start "" http://localhost:5300/
    echo Site opened in your browser. You can close this window.
) else (
    echo.
    echo [info] Timeout waiting (site may still be starting). Open http://localhost:5300/ manually.
)
if exist "%TEMP%\_ih_check.txt" del "%TEMP%\_ih_check.txt" >nul 2>nul
echo.
pause
exit /b 0
