"""
Project Manager - Handles project creation, loading, and saving
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .utils import slugify, ensure_dir


class ProjectManager:
    """Manages novel projects including save/load and versioning"""

    CONFIG_FILENAME = ".novel-config.json"
    OUTPUTS_DIR = "agent-outputs"
    VERSIONS_DIR = "versions"

    AGENTS = {
        "1": {"name": "Architect Agent", "file": "01_ARCHITECT_AGENT.md"},
        "2": {"name": "Prose Stylist Agent", "file": "02_PROSE_STYLIST_AGENT.md"},
        "3": {"name": "Character Psychologist Agent", "file": "03_CHARACTER_PSYCHOLOGIST_AGENT.md"},
        "4": {"name": "Atmosphere & Setting Agent", "file": "04_ATMOSPHERE_SETTING_AGENT.md"},
        "5": {"name": "Research Agent", "file": "05_RESEARCH_AGENT.md"},
        "6": {"name": "Continuity Editor Agent", "file": "06_CONTINUITY_EDITOR_AGENT.md"},
        "7": {"name": "Beta Reader Agent", "file": "07_BETA_READER_AGENT.md"},
        "8": {"name": "Story Advocate Agent", "file": "08_STORY_ADVOCATE_AGENT.md"},
        "9": {"name": "Redundancy Editor Agent", "file": "09_REDUNDANCY_EDITOR_AGENT.md"}
    }

    def __init__(self, framework_root: Path):
        """Initialize project manager with framework root directory"""
        self.framework_root = Path(framework_root)
        self.current_project_dir: Optional[Path] = None
        self.current_config: Optional[Dict] = None

    def create_project(self, name: str, author: str, directory: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Create a new novel project

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            project_dir = Path(directory) if directory else Path.home() / "NovelProjects" / slugify(name)

            # Create directory structure
            ensure_dir(project_dir)

            # Outline folder with revisions
            ensure_dir(project_dir / "outline")
            ensure_dir(project_dir / "outline" / "revisions")

            # Conversations folder (auto-populated by agent_manager)
            ensure_dir(project_dir / "conversations")

            # Manuscript with chapters and scenes
            ensure_dir(project_dir / "manuscript")
            ensure_dir(project_dir / "manuscript" / "chapters")
            ensure_dir(project_dir / "manuscript" / "scenes")

            # Story bible for continuity tracking
            ensure_dir(project_dir / "story-bible")

            # Research and feedback
            ensure_dir(project_dir / "research")
            ensure_dir(project_dir / "feedback")

            # Legacy outputs directory (kept for compatibility)
            ensure_dir(project_dir / self.OUTPUTS_DIR)

            # Versions for snapshots
            ensure_dir(project_dir / self.VERSIONS_DIR)

            # Create initial outline file
            outline_file = project_dir / "outline" / "current-outline.md"
            outline_file.write_text("# Story Outline\n\n*Your outline will appear here as you work with the Architect agent.*\n", encoding='utf-8')

            # Create configuration
            config = {
                "project_name": name,
                "version": "1.0",
                "metadata": {
                    "author": author,
                    "genre": "Literary Fiction",
                    "target_word_count": 80000,
                    "created_date": datetime.now().strftime("%Y-%m-%d"),
                    "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "vision": {
                    "story_idea": "",
                    "themes": [],
                    "tone": "",
                    "style_notes": ""
                },
                "structure": {
                    "pov": "third_person_limited",
                    "chronology": "linear",
                    "estimated_chapters": 20
                },
                "active_phase": "configure",
                "agent_settings": {
                    "mode": "simple",  # simple or advanced
                    "selected_agents": list(self.AGENTS.keys()),
                    "custom_instructions": {}
                }
            }

            config_path = project_dir / self.CONFIG_FILENAME
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

            self.current_project_dir = project_dir
            self.current_config = config

            return True, f"Project created successfully at {project_dir}"

        except Exception as e:
            return False, f"Error creating project: {str(e)}"

    def load_project(self, directory: Path) -> Tuple[bool, str]:
        """
        Load an existing project

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            config_path = Path(directory) / self.CONFIG_FILENAME

            if not config_path.exists():
                return False, f"No project configuration found at {directory}"

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.current_project_dir = Path(directory)
            self.current_config = config

            return True, f"Project loaded: {config.get('project_name', 'Unnamed')}"

        except Exception as e:
            return False, f"Error loading project: {str(e)}"

    def save_project(self) -> Tuple[bool, str]:
        """
        Save current project configuration

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir or not self.current_config:
            return False, "No project loaded"

        try:
            # Update last modified time
            self.current_config["metadata"]["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            config_path = self.current_project_dir / self.CONFIG_FILENAME
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, indent=2)

            return True, "Project saved successfully"

        except Exception as e:
            return False, f"Error saving project: {str(e)}"

    def save_agent_output(self, agent_num: str, content: str) -> Tuple[bool, str]:
        """
        Save output from a specific agent

        Args:
            agent_num: Agent number (1-9)
            content: Agent output content

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir:
            return False, "No project loaded"

        try:
            outputs_dir = self.current_project_dir / self.OUTPUTS_DIR
            ensure_dir(outputs_dir)

            agent_name = self.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")
            filename = f"agent_{agent_num}_{slugify(agent_name)}.md"

            output_path = outputs_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {agent_name} Output\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)

            return True, f"Agent output saved to {filename}"

        except Exception as e:
            return False, f"Error saving agent output: {str(e)}"

    def save_chapter(self, content: str, chapter_name: str = None) -> Tuple[bool, str]:
        """
        Save content as a chapter in manuscript/chapters/ with version history

        Args:
            content: Chapter content
            chapter_name: Optional chapter name (will auto-detect from content if not provided)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir:
            return False, "No project loaded"

        try:
            chapters_dir = self.current_project_dir / "manuscript" / "chapters"
            ensure_dir(chapters_dir)

            # Auto-detect chapter name from content if not provided
            if not chapter_name:
                # Try to extract from first line if it starts with "# Chapter"
                lines = content.strip().split('\n')
                if lines and lines[0].startswith('# Chapter'):
                    chapter_name = slugify(lines[0].replace('#', '').strip())
                else:
                    # Use timestamp if no chapter heading found
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    chapter_name = f"chapter-{timestamp}"
            else:
                chapter_name = slugify(chapter_name)

            # Add .md extension if not present
            if not chapter_name.endswith('.md'):
                chapter_name = f"{chapter_name}.md"

            chapter_path = chapters_dir / chapter_name

            # If chapter already exists, create a version backup
            if chapter_path.exists():
                versions_dir = chapters_dir / "versions"
                ensure_dir(versions_dir)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                # Remove .md extension for version naming
                base_name = chapter_name.replace('.md', '')
                version_path = versions_dir / f"{base_name}-{timestamp}.md"

                # Copy current chapter to versions
                current_content = chapter_path.read_text(encoding='utf-8')
                version_path.write_text(current_content, encoding='utf-8')

            # Write new chapter
            with open(chapter_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, f"Chapter saved to {chapter_name}"

        except Exception as e:
            return False, f"Error saving chapter: {str(e)}"

    def save_outline(self, content: str) -> Tuple[bool, str]:
        """
        Save content as the current outline

        Args:
            content: Outline content

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir:
            return False, "No project loaded"

        try:
            outline_dir = self.current_project_dir / "outline"
            ensure_dir(outline_dir)

            # Save to current-outline.md
            outline_path = outline_dir / "current-outline.md"

            # If outline already exists, create a revision backup
            if outline_path.exists():
                revisions_dir = outline_dir / "revisions"
                ensure_dir(revisions_dir)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                revision_path = revisions_dir / f"outline-{timestamp}.md"

                # Copy current outline to revisions
                current_content = outline_path.read_text(encoding='utf-8')
                revision_path.write_text(current_content, encoding='utf-8')

            # Write new outline
            with open(outline_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, "Outline saved to current-outline.md"

        except Exception as e:
            return False, f"Error saving outline: {str(e)}"

    def load_agent_output(self, agent_num: str) -> Tuple[bool, str, str]:
        """
        Load output from a specific agent

        Returns:
            Tuple of (success: bool, content: str, message: str)
        """
        if not self.current_project_dir:
            return False, "", "No project loaded"

        try:
            outputs_dir = self.current_project_dir / self.OUTPUTS_DIR
            agent_name = self.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")
            filename = f"agent_{agent_num}_{slugify(agent_name)}.md"

            output_path = outputs_dir / filename

            if not output_path.exists():
                return False, "", f"No output found for Agent {agent_num}"

            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return True, content, "Output loaded successfully"

        except Exception as e:
            return False, "", f"Error loading agent output: {str(e)}"

    def save_final_story(self, content: str) -> Tuple[bool, str]:
        """
        Save the final story content

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir:
            return False, "No project loaded"

        try:
            manuscript_dir = self.current_project_dir / "manuscript"
            ensure_dir(manuscript_dir)

            story_path = manuscript_dir / "final_story.md"
            with open(story_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, "Final story saved"

        except Exception as e:
            return False, f"Error saving final story: {str(e)}"

    def load_final_story(self) -> Tuple[bool, str, str]:
        """
        Load the final story content

        Returns:
            Tuple of (success: bool, content: str, message: str)
        """
        if not self.current_project_dir:
            return False, "", "No project loaded"

        try:
            story_path = self.current_project_dir / "manuscript" / "final_story.md"

            if not story_path.exists():
                return False, "", "No final story found"

            with open(story_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return True, content, "Story loaded successfully"

        except Exception as e:
            return False, "", f"Error loading story: {str(e)}"

    def create_version(self, version_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create a version snapshot of the current project state

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.current_project_dir:
            return False, "No project loaded"

        try:
            versions_dir = self.current_project_dir / self.VERSIONS_DIR
            ensure_dir(versions_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_name = version_name or f"version_{timestamp}"
            version_dir = versions_dir / slugify(version_name)

            ensure_dir(version_dir)

            # Copy manuscript and agent outputs
            manuscript_src = self.current_project_dir / "manuscript"
            outputs_src = self.current_project_dir / self.OUTPUTS_DIR

            if manuscript_src.exists():
                shutil.copytree(manuscript_src, version_dir / "manuscript", dirs_exist_ok=True)

            if outputs_src.exists():
                shutil.copytree(outputs_src, version_dir / self.OUTPUTS_DIR, dirs_exist_ok=True)

            # Save version metadata
            version_info = {
                "version_name": version_name,
                "created": timestamp,
                "project_name": self.current_config.get("project_name", "Unknown")
            }

            with open(version_dir / "version_info.json", 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=2)

            return True, f"Version '{version_name}' created"

        except Exception as e:
            return False, f"Error creating version: {str(e)}"

    def list_versions(self) -> List[Dict]:
        """
        List all versions of the current project

        Returns:
            List of version info dictionaries
        """
        if not self.current_project_dir:
            return []

        versions_dir = self.current_project_dir / self.VERSIONS_DIR
        if not versions_dir.exists():
            return []

        versions = []
        for version_dir in sorted(versions_dir.iterdir(), reverse=True):
            if version_dir.is_dir():
                info_file = version_dir / "version_info.json"
                if info_file.exists():
                    with open(info_file, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                        info['path'] = str(version_dir)
                        versions.append(info)

        return versions

    def get_config(self) -> Optional[Dict]:
        """Get current project configuration"""
        return self.current_config

    def update_config(self, updates: Dict) -> None:
        """Update project configuration"""
        if self.current_config:
            self.current_config.update(updates)

    def get_progress_stats(self) -> Dict:
        """
        Get project progress statistics

        Returns:
            Dictionary with word_count, target_word_count, completion_percent
        """
        if not self.current_project_dir:
            return {"word_count": 0, "target_word_count": 0, "completion_percent": 0}

        # Count words in manuscript
        word_count = 0
        manuscript_dir = self.current_project_dir / "manuscript"

        # Count from chapters
        chapters_dir = manuscript_dir / "chapters"
        if chapters_dir.exists():
            for chapter_file in chapters_dir.glob("*.md"):
                content = chapter_file.read_text(encoding='utf-8')
                words = len(content.split())
                word_count += words

        # Count from scenes if no chapters
        if word_count == 0:
            scenes_dir = manuscript_dir / "scenes"
            if scenes_dir.exists():
                for scene_file in scenes_dir.glob("*.md"):
                    content = scene_file.read_text(encoding='utf-8')
                    words = len(content.split())
                    word_count += words

        # Count from final story if nothing else
        if word_count == 0:
            final_story = manuscript_dir / "final_story.md"
            if final_story.exists():
                content = final_story.read_text(encoding='utf-8')
                word_count = len(content.split())

        # Get target from config
        target = self.current_config.get("metadata", {}).get("target_word_count", 80000) if self.current_config else 80000

        # Calculate completion percentage
        completion = (word_count / target * 100) if target > 0 else 0

        return {
            "word_count": word_count,
            "target_word_count": target,
            "completion_percent": min(completion, 100)  # Cap at 100%
        }

    def list_conversations(self) -> List[Dict]:
        """
        List all agent conversations

        Returns:
            List of conversation info dictionaries
        """
        if not self.current_project_dir:
            return []

        conversations = []
        conversations_dir = self.current_project_dir / "conversations"

        if not conversations_dir.exists():
            return []

        # Get full transcript
        transcript_file = conversations_dir / "full-transcript.md"
        if transcript_file.exists():
            conversations.append({
                "type": "transcript",
                "name": "Full Transcript",
                "path": str(transcript_file),
                "agent": "all"
            })

        # Get agent-specific conversations
        for agent_dir in sorted(conversations_dir.iterdir()):
            if agent_dir.is_dir() and agent_dir.name.startswith("agent-"):
                # Extract agent number from directory name (e.g., "agent-1-architect-agent")
                parts = agent_dir.name.split("-")
                if len(parts) >= 2:
                    agent_num = parts[1]
                    agent_name = self.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")

                    # List session files in this agent's directory
                    for session_file in sorted(agent_dir.glob("*.md"), reverse=True):
                        # Parse timestamp from filename
                        timestamp = session_file.stem.replace("-session", "").replace("_", " ")

                        conversations.append({
                            "type": "session",
                            "name": f"{agent_name} - {timestamp}",
                            "path": str(session_file),
                            "agent": agent_num,
                            "agent_name": agent_name,
                            "timestamp": timestamp
                        })

        return conversations
