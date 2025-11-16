"""
API Key Setup Dialog - Dialog for entering Anthropic API key
"""

import customtkinter as ctk
from tkinter import messagebox
import webbrowser

from .api_key_manager import APIKeyManager


class APIKeyDialog(ctk.CTkToplevel):
    """Dialog for setting up Anthropic API key"""

    def __init__(self, parent, api_key_manager: APIKeyManager):
        super().__init__(parent)

        self.api_key_manager = api_key_manager
        self.result = None  # Will be True if key was set, False if cancelled

        self.title("Anthropic API Key Setup")
        self.geometry("600x450")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

        # Center on screen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 450) // 2
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create dialog widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="🔑 Anthropic API Key Required",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        # Info frame
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=30, pady=10)

        info_text = (
            "To use the Novel Writer AI agents, you need an Anthropic API key.\n\n"
            "This key allows the application to communicate with Claude AI.\n"
            "Your key will be saved securely on your computer."
        )

        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 12),
            justify="left",
            wraplength=500
        ).pack(padx=15, pady=15)

        # Get API key button
        get_key_frame = ctk.CTkFrame(self)
        get_key_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            get_key_frame,
            text="Don't have an API key yet?",
            font=("Arial", 11)
        ).pack(side="left", padx=10)

        get_key_btn = ctk.CTkButton(
            get_key_frame,
            text="Get API Key from Anthropic",
            command=self._open_anthropic_console,
            width=200
        )
        get_key_btn.pack(side="right", padx=10, pady=10)

        # API key entry
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            entry_frame,
            text="Enter your Anthropic API Key:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.api_key_entry = ctk.CTkEntry(
            entry_frame,
            width=520,
            height=40,
            placeholder_text="sk-ant-...",
            show="•"  # Hide API key by default
        )
        self.api_key_entry.pack(padx=10, pady=10)

        # Show/hide button
        show_hide_frame = ctk.CTkFrame(entry_frame)
        show_hide_frame.pack(anchor="w", padx=10)

        self.show_var = ctk.BooleanVar(value=False)
        show_cb = ctk.CTkCheckBox(
            show_hide_frame,
            text="Show API key",
            variable=self.show_var,
            command=self._toggle_show_key
        )
        show_cb.pack(side="left")

        # Help text
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=30, pady=10)

        help_text = (
            "💡 Tip: Your API key starts with 'sk-ant-' and is about 100 characters long.\n"
            "It will be saved in ~/.novel_writer/.env"
        )

        ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        ).pack(padx=10, pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=30, pady=20)

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save and Continue",
            command=self._save_key,
            width=180,
            height=40,
            font=("Arial", 13, "bold")
        )
        save_btn.pack(side="right", padx=5)

        skip_btn = ctk.CTkButton(
            button_frame,
            text="Skip for Now",
            command=self._skip,
            width=150,
            height=40,
            fg_color="gray"
        )
        skip_btn.pack(side="right", padx=5)

        # Bind Enter key to save
        self.api_key_entry.bind("<Return>", lambda e: self._save_key())

    def _toggle_show_key(self):
        """Toggle API key visibility"""
        if self.show_var.get():
            self.api_key_entry.configure(show="")
        else:
            self.api_key_entry.configure(show="•")

    def _open_anthropic_console(self):
        """Open Anthropic console in browser"""
        try:
            webbrowser.open("https://console.anthropic.com/settings/keys")
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open browser. Please visit:\n"
                f"https://console.anthropic.com/settings/keys\n\n"
                f"Error: {str(e)}"
            )

    def _save_key(self):
        """Save the API key"""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            messagebox.showwarning(
                "No API Key Entered",
                "Please enter your Anthropic API key or click 'Skip for Now' to continue without it."
            )
            return

        # Basic validation
        if not api_key.startswith("sk-ant-"):
            response = messagebox.askyesno(
                "Unusual API Key Format",
                "Your API key doesn't start with 'sk-ant-' which is unusual for Anthropic keys.\n\n"
                "Are you sure you want to save this key?"
            )
            if not response:
                return

        # Save the key
        success, message = self.api_key_manager.save_api_key(api_key)

        if success:
            self.result = True
            messagebox.showinfo(
                "API Key Saved!",
                "Your API key has been saved successfully!\n\n"
                "You can now use all the AI agents in the application."
            )
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save API key:\n{message}")

    def _skip(self):
        """Skip API key setup"""
        response = messagebox.askyesno(
            "Skip API Key Setup?",
            "Without an API key, you won't be able to use the AI agents.\n\n"
            "You can add it later from the Settings menu.\n\n"
            "Continue without API key?"
        )

        if response:
            self.result = False
            self.destroy()
