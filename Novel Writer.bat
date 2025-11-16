@echo off
REM Novel Writer - Windows Launcher
REM Double-click this file to run the Novel Writer application

echo ====================================
echo Novel Writer - AI Novel Writing System
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "novel_gui.py" (
    echo ERROR: novel_gui.py not found
    echo Please make sure you're running this from the Novel_with_Claude_Agents directory
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Dependencies not installed. Running installer...
    echo.
    python install_gui_wizard.py
    if errorlevel 1 (
        echo.
        echo Installation failed. Please run install_gui_wizard.py manually
        pause
        exit /b 1
    )
)

REM Launch the application
echo.
echo Launching Novel Writer...
echo.
python novel_gui.py

REM If the app exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
