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

    def __init__(self, parent, project_manager: ProjectManager, agent_manager: AgentManager, review_tab=None):
        self.parent = parent
        self.project_manager = project_manager
        self.agent_manager = agent_manager
        self.review_tab = review_tab  # Reference to review tab for auto-refresh

        self.current_agent: Optional[str] = None
        self.full_response = ""

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Main container with left and right panels
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Chat interface (75% width - much bigger!)
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        left_panel.grid_columnconfigure(0, weight=3)  # Give more weight to left panel

        # Right panel - Logs (25% width - smaller)
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        right_panel.configure(width=300)  # Fixed narrower width

        # === LEFT PANEL: Chat Interface ===

        # Quick guide
        guide_frame = ctk.CTkFrame(left_panel, fg_color=("#3B8ED0", "#1F6AA5"))
        guide_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            guide_frame,
            text="💬 How to Use: Select an agent → Click 'Start Conversation' → Chat about your story → Save the output",
            font=("Arial", 10),
            wraplength=600
        ).pack(padx=10, pady=8)

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

        # Multi-line text input box (4 lines tall)
        self.message_entry = ctk.CTkTextbox(
            input_frame,
            height=100,  # Approximately 4 lines
            wrap="word"
        )
        self.message_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        # Bind Ctrl+Return or Cmd+Return to send message
        self.message_entry.bind("<Control-Return>", lambda e: self._send_message())
        self.message_entry.bind("<Command-Return>", lambda e: self._send_message())

        send_btn = ctk.CTkButton(
            input_frame,
            text="Send\n(Ctrl+Enter)",
            command=self._send_message,
            width=100,
            height=100
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

        save_outline_btn = ctk.CTkButton(
            control_frame,
            text="Save Outline",
            command=self._save_as_outline,
            width=100,
            fg_color="#8B4513"
        )
        save_outline_btn.pack(side="right", padx=5)

        save_scene_btn = ctk.CTkButton(
            control_frame,
            text="Save Scene",
            command=self._save_as_scene,
            width=90,
            fg_color="#9B30FF"
        )
        save_scene_btn.pack(side="right", padx=5)

        save_chapter_btn = ctk.CTkButton(
            control_frame,
            text="Save Chapter",
            command=self._save_as_chapter,
            width=100,
            fg_color="#2B7A0B"
        )
        save_chapter_btn.pack(side="right", padx=5)

        save_output_btn = ctk.CTkButton(
            control_frame,
            text="Save Output",
            command=self._save_agent_output,
            width=90
        )
        save_output_btn.pack(side="right", padx=5)

        clear_btn = ctk.CTkButton(
            control_frame,
            text="Clear Chat",
            command=self._clear_conversation,
            width=100,
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
            messagebox.showwarning(
                "No Project Loaded",
                "Please create or open a project first.\n\n" +
                "Click 'New Project' in the menu to get started."
            )
            return

        if not self.agent_manager.is_api_configured():
            messagebox.showerror(
                "API Key Required",
                "No valid Anthropic API key found.\n\n" +
                "To set up your API key:\n" +
                "1. Click 'Settings' in the top menu\n" +
                "2. Click 'Change API Key'\n" +
                "3. Paste your API key and save\n\n" +
                "Get your API key from:\n" +
                "https://console.anthropic.com/settings/keys"
            )
            return

        agent_num = self.agent_var.get().split(".")[0].strip()
        self.current_agent = agent_num

        # Set project directory for auto-saving conversations
        if self.project_manager.current_project_dir:
            self.agent_manager.set_project_directory(self.project_manager.current_project_dir)

        # Get story context from config
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

        # Validate that user has configured their story
        if not story_context["story_idea"].strip():
            response = messagebox.askyesno(
                "Story Not Configured",
                "You haven't filled in your story details yet!\n\n" +
                "For best results, go to the Configure tab and:\n" +
                "1. Describe your story idea\n" +
                "2. Set genre, themes, and other details\n" +
                "3. Save the project\n\n" +
                "Do you want to continue anyway?\n" +
                "(The agent will have limited context)"
            )
            if not response:
                return

        # Start conversation (returns previous messages if continuing)
        previous_messages = self.agent_manager.start_conversation(agent_num, story_context)

        agent_name = self.agent_manager.get_agent_name(agent_num)

        # Display previous conversation history if continuing
        if previous_messages:
            self._add_to_chat(f"[SYSTEM] Continuing conversation with {agent_name} ({len(previous_messages)} previous messages loaded)", "system")
            self._log(f"Continuing conversation with Agent {agent_num}: {agent_name}")
            self._log(f"Loaded {len(previous_messages)} previous messages")

            # Display previous messages in the chat
            for msg in previous_messages:
                if msg["role"] == "user":
                    self._add_to_chat(f"You: {msg['content']}", "user")
                elif msg["role"] == "assistant":
                    self._add_to_chat(f"{agent_name}: {msg['content']}", "agent")
        else:
            self._add_to_chat(f"[SYSTEM] Started new conversation with {agent_name}", "system")
            self._log(f"Started new conversation with Agent {agent_num}: {agent_name}")

        self._log(f"Story context provided:")
        self._log(f"  - Genre: {story_context['genre']}")
        if story_context.get('story_idea'):
            self._log(f"  - Story idea: {story_context['story_idea'][:100]}...")
        if story_context['themes']:
            self._log(f"  - Themes: {', '.join(story_context['themes'])}")

        self.status_label.configure(text=f"Status: Connected to {agent_name}")

    def _send_message(self):
        """Send message to agent"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "Please start a conversation first")
            return

        # Get text from textbox (from start to end, excluding final newline)
        message = self.message_entry.get("1.0", "end-1c").strip()
        if not message:
            return

        # Clear textbox
        self.message_entry.delete("1.0", "end")

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

        # Auto-detect and save chapters/outlines
        self._auto_save_content(full_response)

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

    def _is_narrative_content(self, content: str) -> bool:
        """
        Determine if content is actual narrative prose vs discussion about writing

        Returns True if content appears to be actual story content
        """
        # Check for discussion/meta-writing indicators
        discussion_phrases = [
            'let me', 'i can', 'i will', 'i would', 'i suggest', 'i recommend',
            'here is', 'here are', "here's", 'this chapter', 'this scene',
            'the chapter should', 'you could', 'you should', 'you might',
            'we could', 'we should', 'consider', 'i think', 'perhaps we',
            'what if', 'how about', 'in this chapter', 'for this chapter',
            'regarding', 'concerning', 'my suggestion', 'my recommendation'
        ]

        content_lower = content.lower()
        first_500 = content_lower[:500]

        # If it contains many discussion phrases, it's probably meta-writing
        discussion_count = sum(1 for phrase in discussion_phrases if phrase in first_500)
        if discussion_count >= 3:
            return False

        # Check for narrative indicators
        has_dialogue = content.count('"') >= 4 or content.count("'") >= 4
        has_paragraphs = content.count('\n\n') >= 3
        has_narrative_past_tense = any(word in content_lower for word in [' walked ', ' said ', ' looked ', ' felt ', ' thought ', ' saw ', ' heard '])

        # Check word count - narrative should be substantial
        word_count = len(content.split())

        # Narrative content should have:
        # - Reasonable length (800+ words for chapters)
        # - Multiple paragraphs
        # - Either dialogue or narrative verbs
        if word_count >= 800 and has_paragraphs and (has_dialogue or has_narrative_past_tense):
            return True

        return False

    def _auto_save_content(self, response: str):
        """Automatically detect and save chapters, scenes, or outlines from agent response"""
        # SAFEGUARD: Minimum length requirement - must be substantial
        if not response or len(response.strip()) < 500:
            return  # Too short to be meaningful content

        lines = response.strip().split('\n')
        first_line = lines[0].strip() if lines else ""
        content_lower = response.lower()

        # === CHAPTER DETECTION ===
        # Check multiple chapter formats
        is_chapter = False
        chapter_indicators = [
            '# chapter',
            '## chapter',
            '# ch.',
            '## ch.',
        ]

        # SAFEGUARD: Only detect chapter if it starts with proper heading
        if any(indicator in first_line.lower() for indicator in chapter_indicators):
            is_chapter = True

        if is_chapter:
            # SAFEGUARD: Check if this is actual narrative content vs discussion
            if not self._is_narrative_content(response):
                self._log("[AUTO-SAVE] Skipped - appears to be discussion about chapter, not actual content")
                return

            # SAFEGUARD: For chapters, require minimum 1500 characters
            if len(response) < 1500:
                self._log("[AUTO-SAVE] Skipped - chapter too short (minimum 1500 characters)")
                return

            # Check if chapter already exists
            from pathlib import Path
            chapter_num = self.project_manager._extract_chapter_number(response)
            if chapter_num:
                chapter_path = self.project_manager.current_project_dir / "manuscript" / "chapters" / f"chapter-{chapter_num}.md"

                # SAFEGUARD: If chapter exists, ask for confirmation
                if chapter_path.exists():
                    confirm = messagebox.askyesno(
                        "Confirm Chapter Update",
                        f"Chapter {chapter_num} already exists.\n\n"
                        f"Do you want to overwrite it?\n\n"
                        f"(Previous version will be backed up to versions/)",
                        icon='warning'
                    )
                    if not confirm:
                        self._log(f"[AUTO-SAVE] Cancelled - user declined to overwrite Chapter {chapter_num}")
                        return

            success, message = self.project_manager.save_chapter(response)
            if success:
                self._log(f"[AUTO-SAVE] {message}")
                # Update status briefly
                original_status = self.status_label.cget("text")
                self.status_label.configure(text="✓ Chapter auto-saved", text_color="green")
                self.parent.after(2000, lambda: self.status_label.configure(
                    text=original_status,
                    text_color="gray"
                ))

                # Refresh review tab to show new chapter
                if self.review_tab:
                    self.review_tab.refresh()

                return

        # === SCENE DETECTION ===
        # Check for scene markers
        scene_indicators = ['# scene', '## scene']
        is_scene = any(indicator in first_line.lower() for indicator in scene_indicators)

        if is_scene:
            # SAFEGUARD: Check if this is actual narrative content
            if not self._is_narrative_content(response):
                self._log("[AUTO-SAVE] Skipped - appears to be discussion about scene, not actual content")
                return

            # SAFEGUARD: Scenes should be at least 800 characters
            if len(response) < 800:
                self._log("[AUTO-SAVE] Skipped - scene too short (minimum 800 characters)")
                return

            success, message = self.project_manager.save_scene(response)
            if success:
                self._log(f"[AUTO-SAVE] {message}")
                original_status = self.status_label.cget("text")
                self.status_label.configure(text="✓ Scene auto-saved", text_color="green")
                self.parent.after(2000, lambda: self.status_label.configure(
                    text=original_status,
                    text_color="gray"
                ))

                # Refresh review tab to show new scene
                if self.review_tab:
                    self.review_tab.refresh()

                return

        # === OUTLINE DETECTION ===
        # Check if this looks like an outline
        outline_keywords = ['# outline', '# story outline', '## outline']

        # SAFEGUARD: Only detect if heading is in first line or second line
        first_two_lines = '\n'.join(lines[:2]).lower()
        has_outline_heading = any(keyword in first_two_lines for keyword in outline_keywords)

        if has_outline_heading:
            # Count structure markers
            structure_count = sum([
                content_lower.count('act '),
                content_lower.count('part '),
                content_lower.count('section '),
                content_lower.count('chapter ')
            ])

            # SAFEGUARD: Require substantial structure (5+ markers) and length
            if structure_count >= 5 and len(response) >= 500:
                # SAFEGUARD: Check if outline exists, ask for confirmation
                outline_path = self.project_manager.current_project_dir / "outline" / "current-outline.md"
                if outline_path.exists():
                    confirm = messagebox.askyesno(
                        "Confirm Outline Update",
                        "The outline already exists.\n\n"
                        "Do you want to overwrite it?\n\n"
                        "(Previous version will be backed up to revisions/)",
                        icon='warning'
                    )
                    if not confirm:
                        self._log("[AUTO-SAVE] Cancelled - user declined to overwrite outline")
                        return

                success, message = self.project_manager.save_outline(response)
                if success:
                    self._log(f"[AUTO-SAVE] {message}")
                    original_status = self.status_label.cget("text")
                    self.status_label.configure(text="✓ Outline auto-saved", text_color="green")
                    self.parent.after(2000, lambda: self.status_label.configure(
                        text=original_status,
                        text_color="gray"
                    ))

                    # Refresh review tab to show new outline
                    if self.review_tab:
                        self.review_tab.refresh()

                    return

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
            # Update status label instead of popup
            original_status = self.status_label.cget("text")
            self.status_label.configure(text="✓ Output saved to file", text_color="green")
            # Reset after 3 seconds
            self.parent.after(3000, lambda: self.status_label.configure(
                text=original_status,
                text_color="gray"
            ))
        else:
            self._log(f"Error saving output: {message}")
            messagebox.showerror("Save Error", message)

    def _save_as_chapter(self):
        """Save the agent's output as a chapter"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "No agent conversation active")
            return

        # Get last agent response
        response = self.agent_manager.get_last_agent_response()
        if not response:
            messagebox.showwarning("Warning", "No agent output to save")
            return

        success, message = self.project_manager.save_chapter(response)

        if success:
            self._log(f"Chapter saved: {message}")
            # Update status label
            original_status = self.status_label.cget("text")
            self.status_label.configure(text="✓ Chapter saved", text_color="green")
            # Reset after 3 seconds
            self.parent.after(3000, lambda: self.status_label.configure(
                text=original_status,
                text_color="gray"
            ))

            # Refresh review tab to show new chapter
            if self.review_tab:
                self.review_tab.refresh()
        else:
            self._log(f"Error saving chapter: {message}")
            messagebox.showerror("Save Error", message)

    def _save_as_scene(self):
        """Save the agent's output as a scene"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "No agent conversation active")
            return

        # Get last agent response
        response = self.agent_manager.get_last_agent_response()
        if not response:
            messagebox.showwarning("Warning", "No agent output to save")
            return

        success, message = self.project_manager.save_scene(response)

        if success:
            self._log(f"Scene saved: {message}")
            # Update status label
            original_status = self.status_label.cget("text")
            self.status_label.configure(text="✓ Scene saved", text_color="green")
            # Reset after 3 seconds
            self.parent.after(3000, lambda: self.status_label.configure(
                text=original_status,
                text_color="gray"
            ))

            # Refresh review tab to show new scene
            if self.review_tab:
                self.review_tab.refresh()
        else:
            self._log(f"Error saving scene: {message}")
            messagebox.showerror("Save Error", message)

    def _save_as_outline(self):
        """Save the agent's output as the current outline"""
        if not self.current_agent:
            messagebox.showwarning("Warning", "No agent conversation active")
            return

        # Get last agent response
        response = self.agent_manager.get_last_agent_response()
        if not response:
            messagebox.showwarning("Warning", "No agent output to save")
            return

        success, message = self.project_manager.save_outline(response)

        if success:
            self._log(f"Outline saved: {message}")
            # Update status label
            original_status = self.status_label.cget("text")
            self.status_label.configure(text="✓ Outline saved", text_color="green")
            # Reset after 3 seconds
            self.parent.after(3000, lambda: self.status_label.configure(
                text=original_status,
                text_color="gray"
            ))

            # Refresh review tab to show new outline
            if self.review_tab:
                self.review_tab.refresh()
        else:
            self._log(f"Error saving outline: {message}")
            messagebox.showerror("Save Error", message)

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
