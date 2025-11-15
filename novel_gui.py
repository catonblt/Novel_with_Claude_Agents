#!/usr/bin/env python3
"""
Novel Writer GUI - Multi-Agent Collaborative Novel Writing System

A user-friendly desktop application for writing novels with AI agents.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import NovelWriterGUI


def main():
    """Main entry point for the GUI application"""
    # Get framework root directory
    framework_root = Path(__file__).parent

    # Create and run application
    app = NovelWriterGUI(framework_root)
    app.mainloop()


if __name__ == "__main__":
    main()
