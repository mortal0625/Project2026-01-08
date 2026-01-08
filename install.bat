@echo off
echo.
echo =================================
echo  Project Setup Script
echo =================================
echo.

REM Check if Python is available
py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found. Please install Python 3 and ensure it's in your PATH.
    pause
    exit /b 1
)

REM Check for virtual environment directory
IF NOT EXIST .venv (
    echo [INFO] Virtual environment not found. Creating one...
    py -3 -m venv .venv
    IF %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
) ELSE (
    echo [INFO] Virtual environment already exists.
)

echo.
echo [INFO] Installing required packages from requirements.txt...
call .\.venv\Scripts\activate.bat
pip install -r requirements.txt
IF %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages. Please check requirements.txt and your internet connection.
    pause
    exit /b 1
)

echo.
echo =================================
echo  Installation Complete!
echo =================================
echo.
echo You can now run the backend and frontend servers as instructed previously.
echo.
pause
exit /b 0
