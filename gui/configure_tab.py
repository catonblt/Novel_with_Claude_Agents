"""
Configure Tab - Project configuration and agent setup
"""

import customtkinter as ctk
from typing import Optional

from .project_manager import ProjectManager
from .agent_manager import AgentManager


class ConfigureTab:
    """Configure tab for project settings and agent selection"""

    def __init__(self, parent, project_manager: ProjectManager, agent_manager: AgentManager):
        self.parent = parent
        self.project_manager = project_manager
        self.agent_manager = agent_manager

        self.mode = "simple"  # simple or advanced
        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Scrollable frame for content
        self.scroll_frame = ctk.CTkScrollableFrame(self.parent)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Getting Started Info Panel
        info_frame = ctk.CTkFrame(self.scroll_frame, fg_color=("#3B8ED0", "#1F6AA5"))
        info_frame.pack(fill="x", pady=(0, 20), padx=5)

        ctk.CTkLabel(
            info_frame,
            text="📝 Getting Started",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(
            info_frame,
            text="1. Fill in your story details below\n" +
                 "2. Choose Simple mode (quick) or Advanced mode (detailed)\n" +
                 "3. Click 'Save Project' in the menu when done\n" +
                 "4. Go to Generate tab to start working with agents",
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # Mode selector
        mode_frame = ctk.CTkFrame(self.scroll_frame)
        mode_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            mode_frame,
            text="Configuration Mode:",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10, pady=10)

        self.mode_var = ctk.StringVar(value="simple")
        mode_selector = ctk.CTkSegmentedButton(
            mode_frame,
            values=["Simple", "Advanced"],
            command=self._on_mode_change,
            variable=self.mode_var
        )
        mode_selector.pack(side="left", padx=10, pady=10)

        # Container for mode-specific content
        self.content_frame = ctk.CTkFrame(self.scroll_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Create both mode UIs
        self._create_simple_mode()
        self._create_advanced_mode()

        # Show simple mode by default
        self._show_mode("simple")

    def _create_simple_mode(self):
        """Create simple mode interface"""
        self.simple_frame = ctk.CTkFrame(self.content_frame)

        # Story Idea
        ctk.CTkLabel(
            self.simple_frame,
            text="Story Idea",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        ctk.CTkLabel(
            self.simple_frame,
            text="What is your novel about? Describe the core idea, premise, or concept.",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w", padx=10)

        self.story_idea_text = ctk.CTkTextbox(self.simple_frame, height=150)
        self.story_idea_text.pack(fill="x", padx=10, pady=10)

        # Genre
        genre_frame = ctk.CTkFrame(self.simple_frame)
        genre_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            genre_frame,
            text="Genre:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=(0, 10))

        self.genre_var = ctk.StringVar(value="Literary Fiction")
        genre_menu = ctk.CTkOptionMenu(
            genre_frame,
            values=[
                "Literary Fiction",
                "Mystery",
                "Thriller",
                "Science Fiction",
                "Fantasy",
                "Romance",
                "Historical Fiction",
                "Other"
            ],
            variable=self.genre_var,
            width=200
        )
        genre_menu.pack(side="left")

        # Target word count
        word_count_frame = ctk.CTkFrame(self.simple_frame)
        word_count_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            word_count_frame,
            text="Target Word Count:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=(0, 10))

        self.word_count_var = ctk.StringVar(value="80000")
        word_count_entry = ctk.CTkEntry(
            word_count_frame,
            textvariable=self.word_count_var,
            width=150
        )
        word_count_entry.pack(side="left")

        # Themes
        ctk.CTkLabel(
            self.simple_frame,
            text="Themes (Optional)",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(20, 5), padx=10)

        ctk.CTkLabel(
            self.simple_frame,
            text="What themes or ideas do you want to explore? (comma-separated)",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w", padx=10)

        self.themes_entry = ctk.CTkEntry(
            self.simple_frame,
            placeholder_text="e.g., identity, loss, redemption"
        )
        self.themes_entry.pack(fill="x", padx=10, pady=10)

        # Tone
        ctk.CTkLabel(
            self.simple_frame,
            text="Tone (Optional)",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(20, 5), padx=10)

        self.tone_entry = ctk.CTkEntry(
            self.simple_frame,
            placeholder_text="e.g., dark, contemplative, whimsical"
        )
        self.tone_entry.pack(fill="x", padx=10, pady=10)

    def _create_advanced_mode(self):
        """Create advanced mode interface"""
        self.advanced_frame = ctk.CTkFrame(self.content_frame)

        # Include all simple mode fields
        ctk.CTkLabel(
            self.advanced_frame,
            text="Story Configuration",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        # Story Idea (advanced)
        ctk.CTkLabel(
            self.advanced_frame,
            text="Story Idea:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        self.adv_story_idea_text = ctk.CTkTextbox(self.advanced_frame, height=100)
        self.adv_story_idea_text.pack(fill="x", padx=10, pady=5)

        # Basic settings frame
        basic_frame = ctk.CTkFrame(self.advanced_frame)
        basic_frame.pack(fill="x", padx=10, pady=10)

        # Genre (advanced)
        genre_frame = ctk.CTkFrame(basic_frame)
        genre_frame.pack(side="left", padx=5)

        ctk.CTkLabel(genre_frame, text="Genre:").pack(anchor="w")
        self.adv_genre_var = ctk.StringVar(value="Literary Fiction")
        ctk.CTkOptionMenu(
            genre_frame,
            values=[
                "Literary Fiction", "Mystery", "Thriller",
                "Science Fiction", "Fantasy", "Romance",
                "Historical Fiction", "Other"
            ],
            variable=self.adv_genre_var,
            width=180
        ).pack()

        # Word count (advanced)
        wc_frame = ctk.CTkFrame(basic_frame)
        wc_frame.pack(side="left", padx=5)

        ctk.CTkLabel(wc_frame, text="Target Words:").pack(anchor="w")
        self.adv_word_count_var = ctk.StringVar(value="80000")
        ctk.CTkEntry(wc_frame, textvariable=self.adv_word_count_var, width=120).pack()

        # Structure settings
        ctk.CTkLabel(
            self.advanced_frame,
            text="Narrative Structure",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(20, 5), padx=10)

        structure_frame = ctk.CTkFrame(self.advanced_frame)
        structure_frame.pack(fill="x", padx=10, pady=5)

        # POV
        pov_frame = ctk.CTkFrame(structure_frame)
        pov_frame.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(pov_frame, text="Point of View:").pack(anchor="w")
        self.pov_var = ctk.StringVar(value="third_person_limited")
        ctk.CTkOptionMenu(
            pov_frame,
            values=[
                "first_person",
                "third_person_limited",
                "third_person_omniscient",
                "multiple_pov"
            ],
            variable=self.pov_var,
            width=180
        ).pack()

        # Chronology
        chron_frame = ctk.CTkFrame(structure_frame)
        chron_frame.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(chron_frame, text="Chronology:").pack(anchor="w")
        self.chronology_var = ctk.StringVar(value="linear")
        ctk.CTkOptionMenu(
            chron_frame,
            values=["linear", "non_linear", "frame_narrative"],
            variable=self.chronology_var,
            width=150
        ).pack()

        # Chapters
        chapters_frame = ctk.CTkFrame(structure_frame)
        chapters_frame.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(chapters_frame, text="Est. Chapters:").pack(anchor="w")
        self.chapters_var = ctk.StringVar(value="20")
        ctk.CTkEntry(chapters_frame, textvariable=self.chapters_var, width=80).pack()

        # Themes (advanced)
        ctk.CTkLabel(
            self.advanced_frame,
            text="Themes:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        self.adv_themes_entry = ctk.CTkEntry(self.advanced_frame)
        self.adv_themes_entry.pack(fill="x", padx=10, pady=5)

        # Tone & Style
        ctk.CTkLabel(
            self.advanced_frame,
            text="Tone:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        self.adv_tone_entry = ctk.CTkEntry(self.advanced_frame)
        self.adv_tone_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            self.advanced_frame,
            text="Style Notes:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        self.style_notes_text = ctk.CTkTextbox(self.advanced_frame, height=80)
        self.style_notes_text.pack(fill="x", padx=10, pady=5)

        # Agent selection
        ctk.CTkLabel(
            self.advanced_frame,
            text="Agent Selection",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(20, 5), padx=10)

        ctk.CTkLabel(
            self.advanced_frame,
            text="Select which agents to use in the writing process:",
            font=("Arial", 11),
            text_color="gray"
        ).pack(anchor="w", padx=10)

        self.agent_checkboxes = {}
        agents_frame = ctk.CTkFrame(self.advanced_frame)
        agents_frame.pack(fill="x", padx=10, pady=10)

        for agent_num, agent_info in self.agent_manager.AGENTS.items():
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(
                agents_frame,
                text=f"{agent_num}. {agent_info['name']}",
                variable=var
            )
            cb.pack(anchor="w", pady=3)
            self.agent_checkboxes[agent_num] = var

    def _on_mode_change(self, value):
        """Handle mode change"""
        mode = value.lower()
        self._show_mode(mode)

    def _show_mode(self, mode):
        """Show the selected mode UI"""
        self.mode = mode

        # Hide all mode frames
        self.simple_frame.pack_forget()
        self.advanced_frame.pack_forget()

        # Show selected mode
        if mode == "simple":
            self.simple_frame.pack(fill="both", expand=True)
        else:
            self.advanced_frame.pack(fill="both", expand=True)

    def load_from_config(self):
        """Load configuration from project manager"""
        config = self.project_manager.get_config()
        if not config:
            return

        metadata = config.get("metadata", {})
        vision = config.get("vision", {})
        structure = config.get("structure", {})
        agent_settings = config.get("agent_settings", {})

        # Load into simple mode
        self.story_idea_text.delete("1.0", "end")
        self.story_idea_text.insert("1.0", vision.get("story_idea", ""))

        self.genre_var.set(metadata.get("genre", "Literary Fiction"))
        self.word_count_var.set(str(metadata.get("target_word_count", 80000)))

        themes = vision.get("themes", [])
        self.themes_entry.delete(0, "end")
        if themes:
            self.themes_entry.insert(0, ", ".join(themes))

        self.tone_entry.delete(0, "end")
        self.tone_entry.insert(0, vision.get("tone", ""))

        # Load into advanced mode
        self.adv_story_idea_text.delete("1.0", "end")
        self.adv_story_idea_text.insert("1.0", vision.get("story_idea", ""))

        self.adv_genre_var.set(metadata.get("genre", "Literary Fiction"))
        self.adv_word_count_var.set(str(metadata.get("target_word_count", 80000)))

        self.adv_themes_entry.delete(0, "end")
        if themes:
            self.adv_themes_entry.insert(0, ", ".join(themes))

        self.adv_tone_entry.delete(0, "end")
        self.adv_tone_entry.insert(0, vision.get("tone", ""))

        self.style_notes_text.delete("1.0", "end")
        self.style_notes_text.insert("1.0", vision.get("style_notes", ""))

        self.pov_var.set(structure.get("pov", "third_person_limited"))
        self.chronology_var.set(structure.get("chronology", "linear"))
        self.chapters_var.set(str(structure.get("estimated_chapters", 20)))

        # Load mode
        mode = agent_settings.get("mode", "simple")
        self.mode_var.set(mode.capitalize())
        self._show_mode(mode)

    def save_to_config(self):
        """Save configuration to project manager"""
        config = self.project_manager.get_config()
        if not config:
            return

        # Get values based on current mode
        if self.mode == "simple":
            story_idea = self.story_idea_text.get("1.0", "end-1c").strip()
            genre = self.genre_var.get()
            word_count = int(self.word_count_var.get())
            themes_str = self.themes_entry.get().strip()
            themes = [t.strip() for t in themes_str.split(",")] if themes_str else []
            tone = self.tone_entry.get().strip()
            style_notes = ""
            pov = "third_person_limited"
            chronology = "linear"
            chapters = 20
        else:
            story_idea = self.adv_story_idea_text.get("1.0", "end-1c").strip()
            genre = self.adv_genre_var.get()
            word_count = int(self.adv_word_count_var.get())
            themes_str = self.adv_themes_entry.get().strip()
            themes = [t.strip() for t in themes_str.split(",")] if themes_str else []
            tone = self.adv_tone_entry.get().strip()
            style_notes = self.style_notes_text.get("1.0", "end-1c").strip()
            pov = self.pov_var.get()
            chronology = self.chronology_var.get()
            chapters = int(self.chapters_var.get())

        # Update config
        config["metadata"]["genre"] = genre
        config["metadata"]["target_word_count"] = word_count

        config["vision"]["story_idea"] = story_idea
        config["vision"]["themes"] = themes
        config["vision"]["tone"] = tone
        config["vision"]["style_notes"] = style_notes

        config["structure"]["pov"] = pov
        config["structure"]["chronology"] = chronology
        config["structure"]["estimated_chapters"] = chapters

        config["agent_settings"]["mode"] = self.mode

        # Save selected agents (advanced mode only)
        if self.mode == "advanced":
            selected = [num for num, var in self.agent_checkboxes.items() if var.get()]
            config["agent_settings"]["selected_agents"] = selected

    def get_story_context(self) -> dict:
        """Get story context for agent manager"""
        self.save_to_config()
        config = self.project_manager.get_config()

        if not config:
            return {}

        return {
            "story_idea": config["vision"].get("story_idea", ""),
            "themes": config["vision"].get("themes", []),
            "genre": config["metadata"].get("genre", ""),
            "target_word_count": config["metadata"].get("target_word_count", 80000),
            "tone": config["vision"].get("tone", ""),
            "pov": config["structure"].get("pov", ""),
            "chronology": config["structure"].get("chronology", "")
        }
