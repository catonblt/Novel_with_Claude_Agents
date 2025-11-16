#!/usr/bin/env python3
"""
Novel Writer - GUI Installation Wizard
Installs all required dependencies for the Novel Writer application
"""

import sys
import subprocess
import os
from pathlib import Path

# Check if tkinter is available (comes with Python)
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("WARNING: tkinter not available, using command-line mode")


class InstallerWizard:
    """GUI wizard for installing dependencies"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Novel Writer - Installation Wizard")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        """Create wizard UI"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2b2b2b")
        title_frame.pack(fill="x", pady=(0, 20))

        title = tk.Label(
            title_frame,
            text="📚 Novel Writer Setup",
            font=("Arial", 24, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            title_frame,
            text="Installing required dependencies...",
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="lightgray"
        )
        subtitle.pack(pady=(0, 20))

        # Info text
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=30, pady=10)

        info_text = tk.Label(
            info_frame,
            text="This wizard will install all required Python packages for Novel Writer.\n"
                 "This may take a few minutes depending on your internet connection.",
            font=("Arial", 10),
            justify="left",
            wraplength=500
        )
        info_text.pack(anchor="w")

        # Progress area
        self.log_text = scrolledtext.ScrolledText(
            self.root,
            height=15,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="lightgreen"
        )
        self.log_text.pack(fill="both", expand=True, padx=30, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=540
        )
        self.progress.pack(padx=30, pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=30, pady=(0, 20))

        self.install_btn = tk.Button(
            button_frame,
            text="Install Dependencies",
            command=self.install,
            font=("Arial", 11, "bold"),
            bg="#0078d4",
            fg="white",
            width=20,
            height=2,
            cursor="hand2"
        )
        self.install_btn.pack(side="right", padx=5)

        self.cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.root.destroy,
            font=("Arial", 11),
            width=15,
            height=2
        )
        self.cancel_btn.pack(side="right", padx=5)

    def log(self, message):
        """Add message to log"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()

    def install(self):
        """Install all dependencies"""
        self.install_btn.config(state="disabled")
        self.progress.start()

        self.log("=" * 60)
        self.log("Starting installation...")
        self.log("=" * 60)
        self.log("")

        try:
            # Check Python version
            self.log("Checking Python version...")
            python_version = sys.version.split()[0]
            self.log(f"✓ Python {python_version} detected")
            self.log("")

            # Upgrade pip
            self.log("Upgrading pip...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.log("✓ pip upgraded successfully")
            else:
                self.log(f"⚠ Warning: {result.stderr}")
            self.log("")

            # Install requirements
            requirements_file = Path(__file__).parent / "requirements.txt"

            if requirements_file.exists():
                self.log("Installing dependencies from requirements.txt...")
                self.log("This may take a few minutes...")
                self.log("")

                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                    capture_output=True,
                    text=True
                )

                # Show output
                if result.stdout:
                    for line in result.stdout.split("\n"):
                        if line.strip():
                            self.log(f"  {line}")

                if result.returncode == 0:
                    self.log("")
                    self.log("=" * 60)
                    self.log("✓ Installation completed successfully!")
                    self.log("=" * 60)
                    self.log("")
                    self.log("You can now close this window and run Novel Writer.")

                    self.install_btn.config(text="Installation Complete", bg="green")
                    self.cancel_btn.config(text="Close", command=self.root.destroy)

                    messagebox.showinfo(
                        "Installation Complete",
                        "All dependencies have been installed successfully!\n\n"
                        "You can now run Novel Writer by double-clicking:\n"
                        "  • Windows: 'Novel Writer.bat'\n"
                        "  • Mac: 'Novel Writer.command'\n"
                        "  • Linux: 'novel-writer.sh'"
                    )
                else:
                    self.log("")
                    self.log("✗ Installation failed!")
                    self.log(result.stderr)
                    messagebox.showerror("Installation Failed", "Installation failed. See log for details.")
                    self.install_btn.config(state="normal")
            else:
                self.log("✗ requirements.txt not found!")
                messagebox.showerror("Error", "requirements.txt file not found!")
                self.install_btn.config(state="normal")

        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Installation error: {str(e)}")
            self.install_btn.config(state="normal")
        finally:
            self.progress.stop()

    def run(self):
        """Run the installer wizard"""
        self.root.mainloop()


def cli_install():
    """Command-line installation fallback"""
    print("=" * 60)
    print("Novel Writer - Dependency Installer")
    print("=" * 60)
    print()

    # Check Python version
    print("Checking Python version...")
    python_version = sys.version.split()[0]
    print(f"✓ Python {python_version} detected")
    print()

    # Upgrade pip
    print("Upgrading pip...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        print("✓ pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠ Warning: Could not upgrade pip")
    print()

    # Install requirements
    requirements_file = Path(__file__).parent / "requirements.txt"

    if requirements_file.exists():
        print("Installing dependencies from requirements.txt...")
        print("This may take a few minutes...")
        print()

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True
            )
            print()
            print("=" * 60)
            print("✓ Installation completed successfully!")
            print("=" * 60)
            print()
            print("You can now run Novel Writer by double-clicking:")
            print("  • Windows: 'Novel Writer.bat'")
            print("  • Mac: 'Novel Writer.command'")
            print("  • Linux: 'novel-writer.sh'")
            print()
            return 0
        except subprocess.CalledProcessError as e:
            print()
            print("✗ Installation failed!")
            print(f"Error: {e}")
            return 1
    else:
        print("✗ requirements.txt not found!")
        return 1


if __name__ == "__main__":
    if TKINTER_AVAILABLE and not "--cli" in sys.argv:
        # Run GUI wizard
        wizard = InstallerWizard()
        wizard.run()
    else:
        # Run CLI installer
        exit_code = cli_install()
        input("\nPress Enter to exit...")
        sys.exit(exit_code)
