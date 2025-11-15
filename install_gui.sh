#!/bin/bash
# Installation script for Novel Writer GUI

echo "======================================"
echo "Novel Writer GUI - Installation Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version is compatible"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Set your Anthropic API key:"
echo "   export ANTHROPIC_API_KEY='your-api-key-here'"
echo ""
echo "2. Launch the application:"
echo "   python3 novel_gui.py"
echo ""
echo "3. Read the documentation:"
echo "   - GUI_README.md for GUI usage"
echo "   - README.md for system overview"
echo ""
