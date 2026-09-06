@echo off
chcp 65001 >nul
title Update Internship Data
echo ==============================================
echo   Updating Internship Data ...
echo ==============================================
echo.

rem Change to project root
cd /d "%~dp0"

echo [1/3] Fetching latest internship data...
python collector\run.py
if errorlevel 1 (
    echo.
    echo [warn] Collection was not fully successful, but continuing to commit...
)

echo.
echo [2/3] Committing data to git...
git add data/internships.json data/feed.xml web/public/data/internships.json web/public/feed.xml
git commit -m "chore(data): update internship data" >nul 2>&1
if errorlevel 1 (
    echo [info] No data change, skip commit.
) else (
    echo [ok] Data change committed.
)

echo [3/3] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo [note] Push failed (maybe not logged in / no network). Local data is updated anyway.
) else (
    echo.
    echo [done] Data updated and synced to GitHub.
)

echo.
echo Refresh the website page to see the latest data.
pause
exit /b 0
