"""
Generate Tab - Chat with agents and view real-time generation logs
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from .project_manager import ProjectManager
from .agent_manager import AgentManager
from .utils import format_timestamp


class GenerateTab:
    """Generate tab with chat interface and real-time logs"""

    def __init__(self, parent, project_manager: ProjectManager, agent_manager: AgentManager):
        self.parent = parent
        self.project_manager = project_manager
        self.agent_manager = agent_manager

        self.current_agent: Optional[str] = None
        self.full_response = ""

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Main container with left and right panels
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Chat interface (60% width)
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Right panel - Logs (40% width)
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # === LEFT PANEL: Chat Interface ===

        # Agent selector
        agent_frame = ctk.CTkFrame(left_panel)
        agent_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            agent_frame,
            text="Select Agent:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=(0, 10))

        self.agent_var = ctk.StringVar(value="8")
        agent_menu = ctk.CTkOptionMenu(
            agent_frame,
            values=[f"{num}. {info['name']}" for num, info in self.agent_manager.AGENTS.items()],
            command=self._on_agent_change,
            variable=self.agent_var,
            width=300
        )
        agent_menu.pack(side="left")

        start_btn = ctk.CTkButton(
            agent_frame,
            text="Start Conversation",
            command=self._start_conversation,
            width=150
        )
        start_btn.pack(side="right", padx=10)

        # Chat display
        ctk.CTkLabel(
            left_panel,
            text="Conversation",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.chat_display = ctk.CTkTextbox(
            left_panel,
            font=("Arial", 11),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.chat_display.configure(state="disabled")

        # Chat input
        input_frame = ctk.CTkFrame(left_panel)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.message_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message to the agent..."
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self._send_message())

        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self._send_message,
            width=80
        )
        send_btn.pack(side="right")

        # Control buttons
        control_frame = ctk.CTkFrame(left_panel)
        control_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="Stop Generation",
            command=self._stop_generation,
            fg_color="red",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)

        save_output_btn = ctk.CTkButton(
            control_frame,
            text="Save Agent Output",
            command=self._save_agent_output,
            width=150
        )
        save_output_btn.pack(side="right", padx=5)

        clear_btn = ctk.CTkButton(
            control_frame,
            text="Clear Conversation",
            command=self._clear_conversation,
            width=150,
            fg_color="gray"
        )
        clear_btn.pack(side="right", padx=5)

        # === RIGHT PANEL: Real-time Logs ===

        ctk.CTkLabel(
            right_panel,
            text="Generation Log",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Agent status
        self.status_label = ctk.CTkLabel(
            right_panel,
            text="Status: Idle",
            font=("Arial", 11),
            text_color="gray"
        )
        self.status_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Log display
        self.log_display = ctk.CTkTextbox(
            right_panel,
            font=("Courier", 10),
            wrap="word"
        )
        self.log_display.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_display.configure(state="disabled")

        # Clear log button
        clear_log_btn = ctk.CTkButton(
            right_panel,
            text="Clear Log",
            command=self._clear_log,
            width=100,
            fg_color="gray"
        )
        clear_log_btn.pack(padx=10, pady=(0, 10))

    def _on_agent_change(self, value):
        """Handle agent selection change"""
        # Extract agent number from "1. Agent Name" format
        self.agent_var.set(value.split(".")[0])

    def _start_conversation(self):
        """Start conversation with selected agent"""
        if not self.project_manager.current_project_dir:
            messagebox.showwarning("Warning", "Please create or open a project first")
            return

        if not self.agent_manager.is_api_configured():
            messagebox.showerror(
                "API Not Configured",
                "Claude API is not configured. Please set the ANTHROPIC_API_KEY environment variable."
            )
            return

        agent_num = self.agent_var.get().split(".")[0].strip()
        self.current_agent = agent_num

        # Get story context from configure tab
        from .configure_tab import ConfigureTab
        # We need to get this from the parent - this is a design issue
        # For now, we'll use the config directly
        config = self.project_manager.get_config()
        if not config:
            messagebox.showwarning("Warning", "No project configuration found")
            return

        story_context = {
            "story_idea": config.get("vision", {}).get("story_idea", ""),
            "themes": config.get("vision", {}).get("themes", []),
            "genre": config.get("metadata", {}).get("genre", ""),
            "target_word_count": config.get("metadata", {}).get("target_word_count", 80000)
        }

        # Start conversation
        self.agent_manager.start_conversation(agent_num, story_context)

        agent_name = self.agent_manager.get_agent_name(agent_num)
        self._add_to_chat(f"[SYSTEM] Started conversation with {agent_name}", "system")
        self._log(f"Conversation started with Agent {agent_num}: {agent_name}")
        self._log(f"Story context provided:")
        self._log(f"  - Genre: {story_context['genre']}")
        if story_context['themes']:
            self._log(f"  - Themes: {', '.join(story_context['themes'])}")

        self.status_label.configure(text=f"Status: Connected to {agent_name}")

    def _send_message(self):
        """Send message to agent"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "Please start a conversation first")
            return

        message = self.message_entry.get().strip()
        if not message:
            return

        # Clear entry
        self.message_entry.delete(0, "end")

        # Add to chat
        self._add_to_chat(f"You: {message}", "user")
        self._log(f"User message sent: {message[:100]}...")

        # Update status
        agent_name = self.agent_manager.get_agent_name(self.current_agent)
        self.status_label.configure(text=f"Status: {agent_name} is thinking...")
        self.stop_btn.configure(state="normal")

        # Reset full response
        self.full_response = ""

        # Send to agent
        self.agent_manager.send_message(
            message,
            on_chunk=self._on_response_chunk,
            on_complete=self._on_response_complete,
            on_error=self._on_response_error
        )

    def _on_response_chunk(self, chunk: str):
        """Handle streamed response chunk"""
        self.full_response += chunk

        # Update chat display in real-time
        self.chat_display.configure(state="normal")

        # If this is the first chunk, add agent name
        if len(self.full_response) == len(chunk):
            agent_name = self.agent_manager.get_agent_name(self.current_agent)
            self.chat_display.insert("end", f"\n{agent_name}: ", "agent")

        self.chat_display.insert("end", chunk)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _on_response_complete(self, full_response: str):
        """Handle completed response"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\n\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

        agent_name = self.agent_manager.get_agent_name(self.current_agent)
        self.status_label.configure(text=f"Status: Connected to {agent_name}")
        self.stop_btn.configure(state="disabled")

        self._log(f"Response completed ({len(full_response)} characters)")

    def _on_response_error(self, error: str):
        """Handle response error"""
        self._add_to_chat(f"[ERROR] {error}", "error")
        self._log(f"Error: {error}")

        self.status_label.configure(text="Status: Error occurred")
        self.stop_btn.configure(state="disabled")

        messagebox.showerror("Error", error)

    def _stop_generation(self):
        """Stop current generation"""
        self.agent_manager.stop_generation()
        self._log("Generation stopped by user")
        self.status_label.configure(text="Status: Stopped")
        self.stop_btn.configure(state="disabled")

    def _save_agent_output(self):
        """Save the agent's output"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "No agent conversation active")
            return

        # Get last agent response
        response = self.agent_manager.get_last_agent_response()
        if not response:
            messagebox.showwarning("Warning", "No agent output to save")
            return

        success, message = self.project_manager.save_agent_output(self.current_agent, response)

        if success:
            self._log(f"Agent output saved: {message}")
            messagebox.showinfo("Success", message)
        else:
            self._log(f"Error saving output: {message}")
            messagebox.showerror("Error", message)

    def _clear_conversation(self):
        """Clear the conversation"""
        if messagebox.askyesno("Confirm", "Clear the current conversation?"):
            self.agent_manager.clear_conversation()
            self.current_agent = None

            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.configure(state="disabled")

            self.status_label.configure(text="Status: Idle")
            self._log("Conversation cleared")

    def _clear_log(self):
        """Clear the log display"""
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.configure(state="disabled")

    def _add_to_chat(self, text: str, tag: str = "normal"):
        """Add text to chat display"""
        self.chat_display.configure(state="normal")

        if tag == "system":
            self.chat_display.insert("end", f"{text}\n", "system")
        elif tag == "user":
            self.chat_display.insert("end", f"{text}\n", "user")
        elif tag == "agent":
            self.chat_display.insert("end", f"{text}\n", "agent")
        elif tag == "error":
            self.chat_display.insert("end", f"{text}\n", "error")
        else:
            self.chat_display.insert("end", f"{text}\n")

        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

        # Configure tags for styling
        self.chat_display.tag_config("system", foreground="gray")
        self.chat_display.tag_config("user", foreground="#4A9EFF")
        self.chat_display.tag_config("agent", foreground="#90EE90")
        self.chat_display.tag_config("error", foreground="#FF6B6B")

    def _log(self, message: str):
        """Add message to log display"""
        timestamp = format_timestamp()
        log_entry = f"[{timestamp}] {message}\n"

        self.log_display.configure(state="normal")
        self.log_display.insert("end", log_entry)
        self.log_display.see("end")
        self.log_display.configure(state="disabled")
