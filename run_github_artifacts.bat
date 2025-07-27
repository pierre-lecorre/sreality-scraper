@echo off
setlocal

cd /d C:\Users\33lec\PycharmProjects\sreality-scraper

if not exist "venv\Scripts\activate.bat" (
    echo Activation script not found!
    exit /b 1
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)

py download_github_artifacts.py
if errorlevel 1 (
    echo Script download_github_artifacts.py failed
    exit /b 1
)

echo Script finished successfully

endlocal