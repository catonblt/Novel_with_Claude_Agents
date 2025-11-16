#!/bin/bash
# Novel Writer - Mac Launcher
# Double-click this file to run the Novel Writer application

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "===================================="
echo "Novel Writer - AI Novel Writing System"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8 or higher from:"
    echo "https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "novel_gui.py" ]; then
    echo "ERROR: novel_gui.py not found"
    echo "Please make sure you're running this from the Novel_with_Claude_Agents directory"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import customtkinter" &> /dev/null; then
    echo ""
    echo "Dependencies not installed. Running installer..."
    echo ""
    python3 install_gui_wizard.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "Installation failed. Please run install_gui_wizard.py manually"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Launch the application
echo ""
echo "Launching Novel Writer..."
echo ""
python3 novel_gui.py

# If the app exits with an error, pause to show the error
if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with an error."
    read -p "Press Enter to exit..."
fi
