"""
Review Tab - View and edit story and agent outputs
"""

import customtkinter as ctk
from tkinter import messagebox

from .project_manager import ProjectManager
from .utils import word_count


class ReviewTab:
    """Review tab for viewing and editing outputs"""

    def __init__(self, parent, project_manager: ProjectManager):
        self.parent = parent
        self.project_manager = project_manager

        self.current_selection = "final_story"
        self.unsaved_changes = False

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Top control panel
        control_panel = ctk.CTkFrame(self.parent)
        control_panel.pack(fill="x", padx=10, pady=10)

        # Output selector
        ctk.CTkLabel(
            control_panel,
            text="View Output:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=(10, 10))

        # Build output options
        output_options = ["Final Story"]
        for num, info in self.project_manager.AGENTS.items():
            output_options.append(f"Agent {num}: {info['name']}")

        self.output_var = ctk.StringVar(value="Final Story")
        output_menu = ctk.CTkOptionMenu(
            control_panel,
            values=output_options,
            command=self._on_output_change,
            variable=self.output_var,
            width=300
        )
        output_menu.pack(side="left", padx=5)

        # Load button
        load_btn = ctk.CTkButton(
            control_panel,
            text="Load",
            command=self._load_output,
            width=80
        )
        load_btn.pack(side="left", padx=10)

        # Save button
        self.save_btn = ctk.CTkButton(
            control_panel,
            text="Save Changes",
            command=self._save_changes,
            width=120
        )
        self.save_btn.pack(side="right", padx=10)

        # Stats panel
        stats_frame = ctk.CTkFrame(self.parent)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Words: 0 | Characters: 0",
            font=("Arial", 11),
            text_color="gray"
        )
        self.stats_label.pack(side="left", padx=10, pady=5)

        self.unsaved_indicator = ctk.CTkLabel(
            stats_frame,
            text="",
            font=("Arial", 11, "italic"),
            text_color="orange"
        )
        self.unsaved_indicator.pack(side="right", padx=10, pady=5)

        # Text editor
        editor_frame = ctk.CTkFrame(self.parent)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(
            editor_frame,
            text="Content Editor",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.text_editor = ctk.CTkTextbox(
            editor_frame,
            font=("Arial", 11),
            wrap="word"
        )
        self.text_editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.text_editor.bind("<<Modified>>", self._on_text_modified)

    def _on_output_change(self, value):
        """Handle output selection change"""
        if self.unsaved_changes:
            if not messagebox.askyesno(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to switch anyway?"
            ):
                # Reset to previous selection
                self.output_var.set(self._get_display_name(self.current_selection))
                return

        # Parse selection
        if value == "Final Story":
            self.current_selection = "final_story"
        else:
            # Extract agent number from "Agent X: Name"
            agent_num = value.split(":")[0].replace("Agent ", "").strip()
            self.current_selection = f"agent_{agent_num}"

        self._load_output()

    def _load_output(self):
        """Load the selected output"""
        if not self.project_manager.current_project_dir:
            messagebox.showwarning("Warning", "No project loaded")
            return

        content = ""

        if self.current_selection == "final_story":
            success, content, message = self.project_manager.load_final_story()
            if not success:
                content = "# Final Story\n\nNo content yet. Start generating with agents to create your story."
        else:
            # Extract agent number
            agent_num = self.current_selection.replace("agent_", "")
            success, content, message = self.project_manager.load_agent_output(agent_num)
            if not success:
                agent_name = self.project_manager.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")
                content = f"# {agent_name} Output\n\nNo output yet. Generate content with this agent first."

        # Load into editor
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", content)

        # Reset modified flag
        self.text_editor.edit_modified(False)
        self.unsaved_changes = False
        self.unsaved_indicator.configure(text="")

        # Update stats
        self._update_stats()

    def _save_changes(self):
        """Save changes to current output"""
        if not self.project_manager.current_project_dir:
            messagebox.showwarning("Warning", "No project loaded")
            return

        content = self.text_editor.get("1.0", "end-1c")

        if self.current_selection == "final_story":
            success, message = self.project_manager.save_final_story(content)
        else:
            agent_num = self.current_selection.replace("agent_", "")
            success, message = self.project_manager.save_agent_output(agent_num, content)

        if success:
            self.unsaved_changes = False
            self.unsaved_indicator.configure(text="✓ Saved", text_color="green")
            self.text_editor.edit_modified(False)
            # Clear the saved indicator after 2 seconds
            self.parent.after(2000, lambda: self.unsaved_indicator.configure(text=""))
        else:
            messagebox.showerror("Save Error", message)

    def _on_text_modified(self, event=None):
        """Handle text modification"""
        if self.text_editor.edit_modified():
            self.unsaved_changes = True
            self.unsaved_indicator.configure(text="Unsaved changes")
            self._update_stats()

    def _update_stats(self):
        """Update word count and character count"""
        content = self.text_editor.get("1.0", "end-1c")
        words = word_count(content)
        chars = len(content)

        self.stats_label.configure(text=f"Words: {words:,} | Characters: {chars:,}")

    def _get_display_name(self, selection: str) -> str:
        """Convert internal selection to display name"""
        if selection == "final_story":
            return "Final Story"
        else:
            agent_num = selection.replace("agent_", "")
            agent_name = self.project_manager.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")
            return f"Agent {agent_num}: {agent_name}"

    def refresh(self):
        """Refresh the review tab when project changes"""
        if self.project_manager.current_project_dir:
            self._load_output()
