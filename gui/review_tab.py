"""
Review Tab - View progress, outline, conversations, and manuscript
"""

import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path

from .project_manager import ProjectManager
from .utils import word_count


class ReviewTab:
    """Review tab with progress overview, navigation tree, and content viewer"""

    def __init__(self, parent, project_manager: ProjectManager):
        self.parent = parent
        self.project_manager = project_manager

        self.current_file_path = None
        self.unsaved_changes = False

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets with new layout"""
        # Main container
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # === TOP: Progress Overview Panel ===
        self._create_progress_panel(main_container)

        # === BOTTOM: Split view (Navigation + Content) ===
        content_container = ctk.CTkFrame(main_container)
        content_container.pack(fill="both", expand=True, pady=(10, 0))

        # Left: Navigation tree (30% width)
        nav_frame = ctk.CTkFrame(content_container)
        nav_frame.pack(side="left", fill="both", padx=(0, 5))
        nav_frame.configure(width=300)

        # Right: Content viewer (70% width)
        viewer_frame = ctk.CTkFrame(content_container)
        viewer_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self._create_navigation_tree(nav_frame)
        self._create_content_viewer(viewer_frame)

    def _create_progress_panel(self, parent):
        """Create the progress overview panel at the top"""
        progress_frame = ctk.CTkFrame(parent, height=120)
        progress_frame.pack(fill="x", pady=(0, 10))
        progress_frame.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            progress_frame,
            text="📊 Progress Overview",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        # Stats container
        stats_container = ctk.CTkFrame(progress_frame)
        stats_container.pack(fill="x", padx=15, pady=(0, 10))

        # Word count
        word_frame = ctk.CTkFrame(stats_container)
        word_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            word_frame,
            text="Word Count",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w")

        self.word_count_label = ctk.CTkLabel(
            word_frame,
            text="0",
            font=("Arial", 24, "bold"),
            text_color="#4A9EFF"
        )
        self.word_count_label.pack(anchor="w")

        # Target
        target_frame = ctk.CTkFrame(stats_container)
        target_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            target_frame,
            text="Target",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w")

        self.target_label = ctk.CTkLabel(
            target_frame,
            text="0",
            font=("Arial", 24, "bold")
        )
        self.target_label.pack(anchor="w")

        # Completion %
        completion_frame = ctk.CTkFrame(stats_container)
        completion_frame.pack(side="left")

        ctk.CTkLabel(
            completion_frame,
            text="Completion",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w")

        self.completion_label = ctk.CTkLabel(
            completion_frame,
            text="0%",
            font=("Arial", 24, "bold"),
            text_color="green"
        )
        self.completion_label.pack(anchor="w")

        # Refresh button
        refresh_btn = ctk.CTkButton(
            progress_frame,
            text="↻ Refresh",
            command=self._update_progress_stats,
            width=100,
            height=30
        )
        refresh_btn.pack(side="right", anchor="ne", padx=15, pady=10)

    def _create_navigation_tree(self, parent):
        """Create the navigation tree on the left"""
        # Title
        ctk.CTkLabel(
            parent,
            text="📁 Project Files",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Scrollable tree container
        self.tree_scroll = ctk.CTkScrollableFrame(parent)
        self.tree_scroll.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        # We'll populate this in refresh()

    def _create_content_viewer(self, parent):
        """Create the content viewer on the right"""
        # Header with file info
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=10)

        self.file_title_label = ctk.CTkLabel(
            header_frame,
            text="Select a file from the left",
            font=("Arial", 14, "bold")
        )
        self.file_title_label.pack(side="left", padx=5)

        # Save button
        self.save_btn = ctk.CTkButton(
            header_frame,
            text="💾 Save",
            command=self._save_current_file,
            width=100
        )
        self.save_btn.pack(side="right", padx=5)

        # Content stats
        self.content_stats_label = ctk.CTkLabel(
            parent,
            text="",
            font=("Arial", 10),
            text_color="gray"
        )
        self.content_stats_label.pack(anchor="e", padx=15, pady=(0, 5))

        # Text editor
        self.text_editor = ctk.CTkTextbox(
            parent,
            font=("Arial", 11),
            wrap="word"
        )
        self.text_editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.text_editor.bind("<<Modified>>", self._on_text_modified)

        # Unsaved indicator
        self.unsaved_indicator = ctk.CTkLabel(
            parent,
            text="",
            font=("Arial", 11, "italic"),
            text_color="orange"
        )
        self.unsaved_indicator.pack(anchor="e", padx=15, pady=(0, 10))

    def _populate_navigation_tree(self):
        """Populate the navigation tree with project files"""
        # Clear existing widgets
        for widget in self.tree_scroll.winfo_children():
            widget.destroy()

        if not self.project_manager.current_project_dir:
            ctk.CTkLabel(
                self.tree_scroll,
                text="No project loaded",
                text_color="gray"
            ).pack(pady=20)
            return

        project_dir = self.project_manager.current_project_dir

        # OUTLINE Section
        self._add_tree_section("📝 Outline")
        outline_dir = project_dir / "outline"
        if outline_dir.exists():
            # Current outline
            current_outline = outline_dir / "current-outline.md"
            if current_outline.exists():
                self._add_tree_item("  • Current Outline", current_outline)

            # Outline revisions
            revisions_dir = outline_dir / "revisions"
            if revisions_dir.exists() and any(revisions_dir.glob("*.md")):
                self._add_tree_subsection("  Revisions")
                for revision in sorted(revisions_dir.glob("*.md"), reverse=True):
                    self._add_tree_item(f"    • {revision.stem}", revision)

        # CONVERSATIONS Section
        self._add_tree_section("💬 Conversations")
        conversations = self.project_manager.list_conversations()

        # Full transcript first
        transcript_convs = [c for c in conversations if c.get("type") == "transcript"]
        for conv in transcript_convs:
            self._add_tree_item("  • Full Transcript", Path(conv["path"]), highlight=True)

        # Group by agent
        session_convs = [c for c in conversations if c.get("type") == "session"]
        agents_with_convs = {}
        for conv in session_convs:
            agent_name = conv.get("agent_name", "Unknown")
            if agent_name not in agents_with_convs:
                agents_with_convs[agent_name] = []
            agents_with_convs[agent_name].append(conv)

        for agent_name in sorted(agents_with_convs.keys()):
            self._add_tree_subsection(f"  {agent_name}")
            for conv in agents_with_convs[agent_name][:5]:  # Show last 5 conversations
                timestamp = conv.get("timestamp", "")
                self._add_tree_item(f"    • {timestamp}", Path(conv["path"]))

        # MANUSCRIPT Section
        self._add_tree_section("📖 Manuscript")
        manuscript_dir = project_dir / "manuscript"
        if manuscript_dir.exists():
            # Chapters
            chapters_dir = manuscript_dir / "chapters"
            if chapters_dir.exists() and any(chapters_dir.glob("*.md")):
                self._add_tree_subsection("  Chapters")
                for chapter in sorted(chapters_dir.glob("*.md")):
                    self._add_tree_item(f"    • {chapter.stem}", chapter)

            # Scenes
            scenes_dir = manuscript_dir / "scenes"
            if scenes_dir.exists() and any(scenes_dir.glob("*.md")):
                self._add_tree_subsection("  Scenes")
                for scene in sorted(scenes_dir.glob("*.md")):
                    self._add_tree_item(f"    • {scene.stem}", scene)

            # Final story
            final_story = manuscript_dir / "final_story.md"
            if final_story.exists():
                self._add_tree_item("  • Final Story", final_story, highlight=True)

        # STORY BIBLE Section
        self._add_tree_section("📚 Story Bible")
        story_bible_dir = project_dir / "story-bible"
        if story_bible_dir.exists():
            for bible_file in sorted(story_bible_dir.glob("*.md")):
                self._add_tree_item(f"  • {bible_file.stem}", bible_file)

    def _add_tree_section(self, text):
        """Add a section header to the tree"""
        label = ctk.CTkLabel(
            self.tree_scroll,
            text=text,
            font=("Arial", 13, "bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(15, 5), padx=5)

    def _add_tree_subsection(self, text):
        """Add a subsection header to the tree"""
        label = ctk.CTkLabel(
            self.tree_scroll,
            text=text,
            font=("Arial", 11, "bold"),
            anchor="w",
            text_color="gray"
        )
        label.pack(fill="x", pady=(8, 2), padx=5)

    def _add_tree_item(self, text, file_path: Path, highlight=False):
        """Add a clickable item to the tree"""
        btn = ctk.CTkButton(
            self.tree_scroll,
            text=text,
            command=lambda: self._load_file(file_path),
            anchor="w",
            fg_color=("#3B8ED0", "#1F6AA5") if highlight else "transparent",
            hover_color=("#36719F", "#144870"),
            height=28,
            font=("Arial", 10)
        )
        btn.pack(fill="x", pady=1, padx=5)

    def _load_file(self, file_path: Path):
        """Load a file into the content viewer"""
        if self.unsaved_changes:
            if not messagebox.askyesno(
                "Unsaved Changes",
                "You have unsaved changes. Load anyway?"
            ):
                return

        try:
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)

                self.current_file_path = file_path
                self.file_title_label.configure(text=file_path.name)
                self.unsaved_changes = False
                self.unsaved_indicator.configure(text="")
                self.text_editor.edit_modified(False)

                # Update stats
                words = word_count(content)
                chars = len(content)
                self.content_stats_label.configure(text=f"Words: {words:,} | Characters: {chars:,}")
            else:
                messagebox.showerror("Error", f"File not found: {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def _save_current_file(self):
        """Save the currently open file"""
        if not self.current_file_path:
            messagebox.showwarning("No File", "No file is currently open")
            return

        try:
            content = self.text_editor.get("1.0", "end-1c")
            self.current_file_path.write_text(content, encoding='utf-8')

            self.unsaved_changes = False
            self.unsaved_indicator.configure(text="✓ Saved", text_color="green")
            self.text_editor.edit_modified(False)

            # Clear indicator after 2 seconds
            self.parent.after(2000, lambda: self.unsaved_indicator.configure(text=""))

            # Update progress stats
            self._update_progress_stats()

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")

    def _on_text_modified(self, event=None):
        """Handle text modification"""
        if self.text_editor.edit_modified():
            self.unsaved_changes = True
            self.unsaved_indicator.configure(text="Unsaved changes", text_color="orange")

            # Update word count
            content = self.text_editor.get("1.0", "end-1c")
            words = word_count(content)
            chars = len(content)
            self.content_stats_label.configure(text=f"Words: {words:,} | Characters: {chars:,}")

    def _update_progress_stats(self):
        """Update the progress statistics at the top"""
        stats = self.project_manager.get_progress_stats()

        self.word_count_label.configure(text=f"{stats['word_count']:,}")
        self.target_label.configure(text=f"{stats['target_word_count']:,}")
        self.completion_label.configure(text=f"{stats['completion_percent']:.1f}%")

    def refresh(self):
        """Refresh the review tab when project changes"""
        self._update_progress_stats()
        self._populate_navigation_tree()

        # Clear current file if not in current project
        if self.current_file_path and self.project_manager.current_project_dir:
            if not str(self.current_file_path).startswith(str(self.project_manager.current_project_dir)):
                self.text_editor.delete("1.0", "end")
                self.current_file_path = None
                self.file_title_label.configure(text="Select a file from the left")
                self.content_stats_label.configure(text="")
