"""
Main GUI Window - Novel Writing Application
"""

import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

from .project_manager import ProjectManager
from .agent_manager import AgentManager
from .configure_tab import ConfigureTab
from .generate_tab import GenerateTab
from .review_tab import ReviewTab
from .export_tab import ExportTab
from .api_key_manager import APIKeyManager
from .api_key_dialog import APIKeyDialog


class NovelWriterGUI(ctk.CTk):
    """Main application window for novel writing GUI"""

    def __init__(self, framework_root: Path):
        super().__init__()

        self.framework_root = Path(framework_root)

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window configuration
        self.title("Novel Writer - Multi-Agent Collaborative Writing System")
        self.geometry("1400x900")

        # Initialize managers
        self.api_key_manager = APIKeyManager()
        self.project_manager = ProjectManager(self.framework_root)
        self.agent_manager = AgentManager(self.framework_root)

        # Create UI
        self._create_menu()
        self._create_main_content()

        # Status
        self.current_project_path: Optional[Path] = None

        # Keyboard shortcuts - save silently without popup
        self.bind("<Control-s>", lambda e: self._save_project_silent())
        self.bind("<Command-s>", lambda e: self._save_project_silent())  # Mac

        # Check API key and show setup dialog if needed
        self.after(100, self._check_api_key)

        # Show welcome message on first launch
        self.after(500, self._show_welcome)

    def _create_menu(self):
        """Create menu bar"""
        # Menu frame at top
        menu_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        menu_frame.pack(fill="x", padx=0, pady=0)
        menu_frame.pack_propagate(False)

        # Menu buttons
        btn_new = ctk.CTkButton(
            menu_frame,
            text="New Project",
            command=self._new_project,
            width=120,
            height=30
        )
        btn_new.pack(side="left", padx=10, pady=5)

        btn_open = ctk.CTkButton(
            menu_frame,
            text="Open Project",
            command=self._open_project,
            width=120,
            height=30
        )
        btn_open.pack(side="left", padx=5, pady=5)

        btn_save = ctk.CTkButton(
            menu_frame,
            text="Save Project",
            command=self._save_project,
            width=120,
            height=30
        )
        btn_save.pack(side="left", padx=5, pady=5)

        # Settings button
        btn_settings = ctk.CTkButton(
            menu_frame,
            text="⚙️ Settings",
            command=self._show_settings,
            width=100,
            height=30
        )
        btn_settings.pack(side="left", padx=5, pady=5)

        # Project name label (on right)
        self.project_name_label = ctk.CTkLabel(
            menu_frame,
            text="No project loaded",
            font=("Arial", 12, "italic")
        )
        self.project_name_label.pack(side="right", padx=20, pady=5)

        # API key status indicator
        self.api_status_label = ctk.CTkLabel(
            menu_frame,
            text="",
            font=("Arial", 10),
            text_color="gray"
        )
        self.api_status_label.pack(side="right", padx=5, pady=5)
        self._update_api_status()

    def _create_main_content(self):
        """Create main content area with tabs"""
        # Create tab view
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.tabview.add("Configure")
        self.tabview.add("Generate")
        self.tabview.add("Review")
        self.tabview.add("Export")

        # Initialize tab contents
        self.configure_tab = ConfigureTab(
            self.tabview.tab("Configure"),
            self.project_manager,
            self.agent_manager
        )

        self.generate_tab = GenerateTab(
            self.tabview.tab("Generate"),
            self.project_manager,
            self.agent_manager
        )

        self.review_tab = ReviewTab(
            self.tabview.tab("Review"),
            self.project_manager
        )

        self.export_tab = ExportTab(
            self.tabview.tab("Export"),
            self.project_manager
        )

    def _new_project(self):
        """Create a new project"""
        dialog = NewProjectDialog(self)
        dialog.wait_window()

        if dialog.result:
            name, author, directory = dialog.result

            success, message = self.project_manager.create_project(name, author, directory)

            if success:
                self.current_project_path = self.project_manager.current_project_dir
                self._update_project_display()

                # Switch to Configure tab to guide user
                self.tabview.set("Configure")
            else:
                messagebox.showerror("Error", message)

    def _open_project(self):
        """Open an existing project"""
        directory = filedialog.askdirectory(
            title="Select Project Directory (containing .novel-config.json)",
            initialdir=Path.home() / "NovelProjects" if (Path.home() / "NovelProjects").exists() else Path.home()
        )

        if directory:
            success, message = self.project_manager.load_project(Path(directory))

            if success:
                self.current_project_path = Path(directory)
                self._update_project_display()
                # Show brief success in status
                project_name = self.project_manager.get_config().get("project_name", "Project")
                self.project_name_label.configure(text=f"✓ {project_name} loaded")
                self.after(2000, self._update_project_display_name_only)
            else:
                messagebox.showerror("Error", f"{message}\n\nMake sure you selected the correct project directory.")

    def _save_project(self):
        """Save current project with confirmation message"""
        if not self.project_manager.current_project_dir:
            messagebox.showwarning("No Project", "Please create or open a project first.")
            return

        # Update config from configure tab
        self.configure_tab.save_to_config()

        success, message = self.project_manager.save_project()

        if success:
            # Show brief success message
            self.project_name_label.configure(text=f"✓ {self.project_manager.get_config().get('project_name', 'Project')} (saved)")
            # Reset after 2 seconds
            self.after(2000, self._update_project_display_name_only)
        else:
            messagebox.showerror("Save Error", message)

    def _save_project_silent(self):
        """Save current project silently (for keyboard shortcut)"""
        if not self.project_manager.current_project_dir:
            # Don't show annoying popup for keyboard shortcut
            return

        # Update config from configure tab
        self.configure_tab.save_to_config()

        success, message = self.project_manager.save_project()

        if success:
            # Just update the status label briefly
            original_text = self.project_name_label.cget("text")
            self.project_name_label.configure(text=f"✓ Saved")
            # Reset after 1.5 seconds
            self.after(1500, lambda: self.project_name_label.configure(text=original_text))
        # Silently fail - user can use Save Project button for explicit feedback

    def _update_project_display(self):
        """Update UI to reflect loaded project"""
        config = self.project_manager.get_config()
        if config:
            project_name = config.get("project_name", "Unknown Project")
            self.project_name_label.configure(text=f"Project: {project_name}")

            # Refresh all tabs
            self.configure_tab.load_from_config()
            self.review_tab.refresh()
            self.export_tab.refresh()

    def _update_project_display_name_only(self):
        """Update just the project name label without refreshing tabs"""
        config = self.project_manager.get_config()
        if config:
            project_name = config.get("project_name", "Unknown Project")
            self.project_name_label.configure(text=f"Project: {project_name}")

    def _check_api_key(self):
        """Check if API key is configured and show setup dialog if not"""
        if not self.api_key_manager.is_configured():
            dialog = APIKeyDialog(self, self.api_key_manager)
            dialog.wait_window()
            self._update_api_status()

    def _update_api_status(self):
        """Update API key status indicator"""
        if self.api_key_manager.is_configured():
            self.api_status_label.configure(
                text="✓ API Key Configured",
                text_color="green"
            )
        else:
            self.api_status_label.configure(
                text="⚠ No API Key",
                text_color="orange"
            )

    def _show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self, self.api_key_manager)
        dialog.wait_window()
        self._update_api_status()

    def _show_welcome(self):
        """Show welcome message on first launch"""
        # Don't show annoying welcome popup - the UI is self-explanatory
        pass


class NewProjectDialog(ctk.CTkToplevel):
    """Dialog for creating a new project"""

    def __init__(self, parent):
        super().__init__(parent)

        self.result = None

        self.title("Create New Project")
        self.geometry("500x400")  # Increased height to show buttons
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create dialog widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Create New Novel Project",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=30, pady=10)

        # Project name
        ctk.CTkLabel(form_frame, text="Project Name:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.name_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="My First Novel")
        self.name_entry.pack(pady=(0, 15))

        # Author name
        ctk.CTkLabel(form_frame, text="Author Name:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.author_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Your Name")
        self.author_entry.pack(pady=(0, 15))

        # Directory
        ctk.CTkLabel(form_frame, text="Project Directory (optional):", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))

        # Show default location
        default_loc = Path.home() / "NovelProjects"
        ctk.CTkLabel(
            form_frame,
            text=f"Default: {default_loc}",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 5))

        dir_frame = ctk.CTkFrame(form_frame)
        dir_frame.pack(fill="x", pady=(0, 15))

        self.directory_entry = ctk.CTkEntry(dir_frame, width=320, placeholder_text="Leave blank to use default location")
        self.directory_entry.pack(side="left", padx=(0, 10))

        browse_btn = ctk.CTkButton(dir_frame, text="Browse", command=self._browse_directory, width=70)
        browse_btn.pack(side="left")

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=30, pady=20)

        create_btn = ctk.CTkButton(
            button_frame,
            text="Create Project",
            command=self._create,
            width=150
        )
        create_btn.pack(side="right", padx=5)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=150,
            fg_color="gray"
        )
        cancel_btn.pack(side="right", padx=5)

    def _browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory(title="Select Project Location")
        if directory:
            self.directory_entry.delete(0, "end")
            self.directory_entry.insert(0, directory)

    def _create(self):
        """Create project with entered information"""
        name = self.name_entry.get().strip()
        author = self.author_entry.get().strip()
        directory = self.directory_entry.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Please enter a project name")
            return

        if not author:
            author = "Your Name"

        self.result = (name, author, Path(directory) if directory else None)
        self.destroy()


class SettingsDialog(ctk.CTkToplevel):
    """Dialog for application settings"""

    def __init__(self, parent, api_key_manager: APIKeyManager):
        super().__init__(parent)

        self.api_key_manager = api_key_manager

        self.title("Settings")
        self.geometry("500x300")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create dialog widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        # Settings frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # API Key section
        ctk.CTkLabel(
            settings_frame,
            text="Anthropic API Key",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Status
        if self.api_key_manager.is_configured():
            status_text = "✓ API key is configured"
            status_color = "green"
        else:
            status_text = "⚠ No API key configured"
            status_color = "orange"

        ctk.CTkLabel(
            settings_frame,
            text=status_text,
            text_color=status_color,
            font=("Arial", 11)
        ).pack(anchor="w", padx=15, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.pack(anchor="w", padx=15, pady=10)

        change_key_btn = ctk.CTkButton(
            button_frame,
            text="Change API Key",
            command=self._change_api_key,
            width=150
        )
        change_key_btn.pack(side="left", padx=5)

        if self.api_key_manager.is_configured():
            clear_key_btn = ctk.CTkButton(
                button_frame,
                text="Remove API Key",
                command=self._clear_api_key,
                width=150,
                fg_color="red"
            )
            clear_key_btn.pack(side="left", padx=5)

        # Close button
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=120
        )
        close_btn.pack(pady=20)

    def _change_api_key(self):
        """Show API key setup dialog"""
        dialog = APIKeyDialog(self, self.api_key_manager)
        dialog.wait_window()
        self.destroy()  # Close settings after changing key

    def _clear_api_key(self):
        """Clear the API key"""
        response = messagebox.askyesno(
            "Confirm Removal",
            "Are you sure you want to remove your API key?\n\n" +
            "You won't be able to use AI agents until you add a new key."
        )

        if response:
            success, message = self.api_key_manager.clear_api_key()
            if success:
                messagebox.showinfo("API Key Removed", "Your API key has been removed successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", f"Failed to remove API key:\n{message}")
