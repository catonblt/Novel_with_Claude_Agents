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
            ensure_dir(project_dir / "planning")
            ensure_dir(project_dir / "manuscript")
            ensure_dir(project_dir / "story-bible")
            ensure_dir(project_dir / "feedback")
            ensure_dir(project_dir / "research")
            ensure_dir(project_dir / self.OUTPUTS_DIR)
            ensure_dir(project_dir / self.VERSIONS_DIR)

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
            with open(config_path, 'w') as f:
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

            with open(config_path, 'r') as f:
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
            with open(config_path, 'w') as f:
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
            with open(output_path, 'w') as f:
                f.write(f"# {agent_name} Output\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)

            return True, f"Agent output saved to {filename}"

        except Exception as e:
            return False, f"Error saving agent output: {str(e)}"

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

            with open(output_path, 'r') as f:
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
            with open(story_path, 'w') as f:
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

            with open(story_path, 'r') as f:
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

            with open(version_dir / "version_info.json", 'w') as f:
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
                    with open(info_file, 'r') as f:
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
