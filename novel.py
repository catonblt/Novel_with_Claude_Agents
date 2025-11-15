#!/usr/bin/env python3
"""
Novel Writing CLI - Interactive tool for the 9-agent collaborative novel writing system

This CLI helps you manage novel projects, interact with agents, and track your writing progress.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class NovelCLI:
    """Main CLI interface for the novel writing system"""

    CONFIG_FILENAME = ".novel-config.json"
    AGENTS_DIR = "agents"
    TEMPLATES_DIR = "templates"

    AGENTS = {
        "1": {"name": "Architect Agent", "file": "01_ARCHITECT_AGENT.md", "role": "Narrative Structure & Thematic Orchestrator"},
        "2": {"name": "Prose Stylist Agent", "file": "02_PROSE_STYLIST_AGENT.md", "role": "Sentence-Level Craftsperson & Voice Keeper"},
        "3": {"name": "Character Psychologist Agent", "file": "03_CHARACTER_PSYCHOLOGIST_AGENT.md", "role": "Interior Life Architect & Dialogue Specialist"},
        "4": {"name": "Atmosphere & Setting Agent", "file": "04_ATMOSPHERE_SETTING_AGENT.md", "role": "Environmental Designer & Sensory World Builder"},
        "5": {"name": "Research Agent", "file": "05_RESEARCH_AGENT.md", "role": "Accuracy Specialist & Cultural Reference Curator"},
        "6": {"name": "Continuity Editor Agent", "file": "06_CONTINUITY_EDITOR_AGENT.md", "role": "Internal Consistency Guardian & Detail Tracker"},
        "7": {"name": "Beta Reader Agent", "file": "07_BETA_READER_AGENT.md", "role": "Critical Reader & Narrative Effectiveness Analyst"},
        "8": {"name": "Story Advocate Agent", "file": "08_STORY_ADVOCATE_AGENT.md", "role": "Human Liaison & Narrative Plausibility Counselor"},
        "9": {"name": "Redundancy Editor Agent", "file": "09_REDUNDANCY_EDITOR_AGENT.md", "role": "Redundancy Detective & Variation Specialist"}
    }

    def __init__(self, framework_root: Optional[Path] = None):
        """Initialize the CLI with the framework root directory"""
        if framework_root:
            self.framework_root = Path(framework_root)
        else:
            self.framework_root = Path(__file__).parent

        self.current_project: Optional[Dict] = None
        self.project_config_path: Optional[Path] = None

    def find_project_config(self, start_dir: Optional[Path] = None) -> Optional[Path]:
        """Find the nearest .novel-config.json file by walking up directories"""
        current = Path(start_dir) if start_dir else Path.cwd()

        while current != current.parent:
            config_path = current / self.CONFIG_FILENAME
            if config_path.exists():
                return config_path
            current = current.parent

        return None

    def load_project(self, config_path: Optional[Path] = None) -> bool:
        """Load a project configuration"""
        if not config_path:
            config_path = self.find_project_config()

        if not config_path:
            return False

        try:
            with open(config_path, 'r') as f:
                self.current_project = json.load(f)
                self.project_config_path = config_path
                return True
        except Exception as e:
            print(f"Error loading project config: {e}")
            return False

    def save_project(self) -> bool:
        """Save the current project configuration"""
        if not self.project_config_path or not self.current_project:
            print("No project loaded to save")
            return False

        try:
            with open(self.project_config_path, 'w') as f:
                json.dump(self.current_project, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project config: {e}")
            return False

    def cmd_init(self, args):
        """Initialize a new novel project"""
        project_name = args.name
        project_dir = Path(args.directory) if args.directory else Path.cwd() / self._slugify(project_name)

        print(f"\n📚 Initializing new novel project: {project_name}")
        print(f"📁 Location: {project_dir}")

        # Create project directory structure
        dirs = {
            "planning": project_dir / "planning",
            "manuscript": project_dir / "manuscript",
            "story_bible": project_dir / "story-bible",
            "feedback": project_dir / "feedback",
            "research": project_dir / "research"
        }

        for name, path in dirs.items():
            path.mkdir(parents=True, exist_ok=True)
            # Create README in each directory
            readme_path = path / "README.md"
            if not readme_path.exists():
                readme_path.write_text(f"# {name.replace('_', ' ').title()}\n\nThis directory contains {name.replace('_', ' ')} for the novel.\n")

        # Create configuration file
        config = {
            "project_name": project_name,
            "version": "1.0",
            "metadata": {
                "author": args.author or "Your Name",
                "genre": "Literary Fiction",
                "target_word_count": 80000,
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "comp_titles": []
            },
            "vision": {
                "themes": [],
                "tone": "",
                "style_notes": "",
                "central_question": "",
                "emotional_core": ""
            },
            "structure": {
                "pov": "third_person_limited",
                "chronology": "linear",
                "estimated_chapters": 20,
                "act_structure": ""
            },
            "workflow_preference": "iterative_spiraling",
            "active_phase": "vision",
            "project_paths": {
                "project_root": str(project_dir),
                "planning_dir": str(dirs["planning"]),
                "manuscript_dir": str(dirs["manuscript"]),
                "story_bible_dir": str(dirs["story_bible"]),
                "feedback_dir": str(dirs["feedback"])
            },
            "custom_notes": {}
        }

        config_path = project_dir / self.CONFIG_FILENAME
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        # Copy templates
        templates_src = self.framework_root / self.TEMPLATES_DIR
        if templates_src.exists():
            templates_dst = project_dir / "templates"
            templates_dst.mkdir(exist_ok=True)
            for template_file in templates_src.glob("*.md"):
                (templates_dst / template_file.name).write_text(template_file.read_text())

        print("\n✅ Project initialized successfully!")
        print(f"\n📋 Next steps:")
        print(f"   1. cd {project_dir}")
        print(f"   2. Edit {self.CONFIG_FILENAME} to refine your vision")
        print(f"   3. Run: python novel.py agent 8  (Start with Story Advocate)")
        print(f"   4. Read the agent instructions and begin your vision discussion")

    def cmd_status(self, args):
        """Show project status"""
        if not self.load_project():
            print("❌ No project found. Run 'novel.py init <name>' to create a new project.")
            return

        p = self.current_project
        print("\n" + "="*60)
        print(f"📚 {p['project_name']}")
        print("="*60)

        # Metadata
        meta = p.get('metadata', {})
        print(f"\n👤 Author: {meta.get('author', 'Not set')}")
        print(f"📖 Genre: {meta.get('genre', 'Not set')}")
        print(f"🎯 Target: {meta.get('target_word_count', 0):,} words")
        print(f"📅 Created: {meta.get('created_date', 'Unknown')}")

        # Current phase
        phase = p.get('active_phase', 'vision')
        print(f"\n🔄 Current Phase: {phase.upper()}")

        # Vision summary
        vision = p.get('vision', {})
        if vision.get('themes'):
            print(f"\n💡 Themes:")
            for theme in vision['themes']:
                print(f"   • {theme}")

        # Structure
        structure = p.get('structure', {})
        if structure.get('pov'):
            print(f"\n📐 Structure:")
            print(f"   • POV: {structure.get('pov', 'Not set').replace('_', ' ').title()}")
            print(f"   • Chronology: {structure.get('chronology', 'Not set').title()}")
            print(f"   • Estimated Chapters: {structure.get('estimated_chapters', 'Not set')}")

        # Workflow
        workflow = p.get('workflow_preference', 'Not set')
        print(f"\n⚙️  Workflow: {workflow.replace('_', ' ').title()}")

        # Project location
        paths = p.get('project_paths', {})
        if paths.get('project_root'):
            print(f"\n📁 Project Root: {paths['project_root']}")

        print("\n" + "="*60 + "\n")

    def cmd_agent(self, args):
        """Display agent information and instructions"""
        agent_num = str(args.number)

        if agent_num not in self.AGENTS:
            print(f"❌ Invalid agent number. Choose 1-9.")
            self._list_agents()
            return

        agent = self.AGENTS[agent_num]
        agent_file = self.framework_root / self.AGENTS_DIR / agent['file']

        if not agent_file.exists():
            print(f"❌ Agent file not found: {agent_file}")
            return

        print("\n" + "="*70)
        print(f"🤖 Agent {agent_num}: {agent['name']}")
        print(f"📋 Role: {agent['role']}")
        print("="*70 + "\n")

        # Read and display agent file
        content = agent_file.read_text()
        print(content)

        print("\n" + "="*70)
        print(f"\n💬 You are now working with {agent['name']}")
        print(f"   Copy the instructions above and paste them into your Claude conversation.")
        print(f"   Then describe what you need help with for your novel.\n")

    def cmd_agents(self, args):
        """List all available agents"""
        self._list_agents()

    def _list_agents(self):
        """Helper to list all agents"""
        print("\n📋 Available Agents:\n")
        for num, agent in self.AGENTS.items():
            print(f"   {num}. {agent['name']}")
            print(f"      {agent['role']}\n")

    def cmd_phase(self, args):
        """Update the current project phase"""
        if not self.load_project():
            print("❌ No project found.")
            return

        phases = ["vision", "planning", "development", "drafting", "revision", "polish"]
        new_phase = args.phase.lower()

        if new_phase not in phases:
            print(f"❌ Invalid phase. Choose from: {', '.join(phases)}")
            return

        old_phase = self.current_project.get('active_phase', 'unknown')
        self.current_project['active_phase'] = new_phase

        if self.save_project():
            print(f"\n✅ Phase updated: {old_phase} → {new_phase}")
            print(f"\n   Recommended agents for '{new_phase}' phase:")
            self._recommend_agents_for_phase(new_phase)

    def _recommend_agents_for_phase(self, phase: str):
        """Recommend agents based on phase"""
        recommendations = {
            "vision": ["8 (Story Advocate)"],
            "planning": ["1 (Architect)", "8 (Story Advocate)"],
            "development": ["3 (Character Psychologist)", "4 (Atmosphere & Setting)",
                          "5 (Research)", "6 (Continuity Editor)"],
            "drafting": ["2 (Prose Stylist)", "3 (Character Psychologist)",
                        "4 (Atmosphere & Setting)", "6 (Continuity Editor)"],
            "revision": ["7 (Beta Reader)", "1 (Architect)", "9 (Redundancy Editor)",
                        "6 (Continuity Editor)"],
            "polish": ["2 (Prose Stylist)", "6 (Continuity Editor)", "7 (Beta Reader)"]
        }

        for agent in recommendations.get(phase, []):
            print(f"      • Agent {agent}")

    def cmd_config(self, args):
        """Edit project configuration"""
        if not self.load_project():
            print("❌ No project found.")
            return

        print(f"\n📝 Project configuration file: {self.project_config_path}")
        print(f"\nTo edit, open this file in your text editor:")
        print(f"   {self.project_config_path}\n")

        if args.show:
            print("Current configuration:")
            print(json.dumps(self.current_project, indent=2))

    def cmd_template(self, args):
        """Show available templates"""
        if not self.load_project():
            print("❌ No project found.")
            return

        templates_dir = self.framework_root / self.TEMPLATES_DIR

        if not templates_dir.exists():
            print(f"❌ Templates directory not found: {templates_dir}")
            return

        templates = list(templates_dir.glob("*.md"))

        if not templates:
            print(f"❌ No templates found in {templates_dir}")
            return

        print("\n📄 Available Templates:\n")
        for i, template in enumerate(templates, 1):
            print(f"   {i}. {template.stem.replace('-', ' ').title()}")
            print(f"      {template.name}\n")

        print(f"Template files are located at: {templates_dir}")
        print(f"Copy these to your project directory when needed.\n")

    def _slugify(self, text: str) -> str:
        """Convert text to a filesystem-safe slug"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Novel Writing CLI - Collaborative novel writing with 9 AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  novel.py init "My First Novel" --author "Jane Doe"
  novel.py status
  novel.py agent 8
  novel.py phase drafting
  novel.py agents

For more help, visit the README.md or USAGE.md documentation.
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new novel project')
    init_parser.add_argument('name', help='Name of your novel project')
    init_parser.add_argument('--directory', '-d', help='Directory to create project in (default: ./project-name)')
    init_parser.add_argument('--author', '-a', help='Author name')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show current project status')

    # Agent command
    agent_parser = subparsers.add_parser('agent', help='Display agent instructions')
    agent_parser.add_argument('number', type=int, help='Agent number (1-9)')

    # Agents list command
    agents_parser = subparsers.add_parser('agents', help='List all available agents')

    # Phase command
    phase_parser = subparsers.add_parser('phase', help='Update project phase')
    phase_parser.add_argument('phase', help='Phase name (vision, planning, development, drafting, revision, polish)')

    # Config command
    config_parser = subparsers.add_parser('config', help='View/edit project configuration')
    config_parser.add_argument('--show', action='store_true', help='Show current configuration')

    # Template command
    template_parser = subparsers.add_parser('templates', help='List available templates')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cli = NovelCLI()

    # Route to appropriate command
    command_map = {
        'init': cli.cmd_init,
        'status': cli.cmd_status,
        'agent': cli.cmd_agent,
        'agents': cli.cmd_agents,
        'phase': cli.cmd_phase,
        'config': cli.cmd_config,
        'templates': cli.cmd_template
    }

    if args.command in command_map:
        command_map[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
