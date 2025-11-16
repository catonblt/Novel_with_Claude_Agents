"""
Agent Manager - Handles agent interactions and Claude API communication
"""

import os
import threading
from pathlib import Path
from typing import Callable, Dict, List, Optional

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AgentManager:
    """Manages AI agent interactions and Claude API communication"""

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
        """Initialize agent manager"""
        self.framework_root = Path(framework_root)
        self.agents_dir = self.framework_root / "agents"
        self.client: Optional[Anthropic] = None
        self.conversation_history: List[Dict] = []
        self.current_agent: Optional[str] = None
        self.current_project_dir: Optional[Path] = None
        self.conversation_session_file: Optional[Path] = None
        self.is_generating = False
        self.stop_requested = False

        # Initialize Anthropic client if available
        if ANTHROPIC_AVAILABLE:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.client = Anthropic(api_key=api_key)

    def set_project_directory(self, project_dir: Path):
        """Set the current project directory for auto-saving conversations"""
        self.current_project_dir = Path(project_dir)

    def _load_project_files(self) -> str:
        """Load all relevant project files to provide context to agents"""
        if not self.current_project_dir:
            return ""

        context_parts = []

        # Load current outline
        outline_file = self.current_project_dir / "outline" / "current-outline.md"
        if outline_file.exists():
            try:
                outline_content = outline_file.read_text(encoding='utf-8')
                context_parts.append("\n## Current Outline\n\n")
                context_parts.append(outline_content)
                context_parts.append("\n")
            except Exception as e:
                print(f"[Agent Manager] Error loading outline: {e}")

        # Load story bible
        story_bible_dir = self.current_project_dir / "story-bible"
        if story_bible_dir.exists():
            bible_files = sorted(story_bible_dir.glob("*.md"))
            if bible_files:
                context_parts.append("\n## Story Bible\n\n")
                for bible_file in bible_files:
                    try:
                        bible_content = bible_file.read_text(encoding='utf-8')
                        context_parts.append(f"### {bible_file.stem}\n\n")
                        context_parts.append(bible_content)
                        context_parts.append("\n")
                    except Exception as e:
                        print(f"[Agent Manager] Error loading {bible_file.name}: {e}")

        # Load existing chapters
        chapters_dir = self.current_project_dir / "manuscript" / "chapters"
        if chapters_dir.exists():
            chapter_files = sorted(chapters_dir.glob("*.md"))
            if chapter_files:
                context_parts.append("\n## Existing Chapters\n\n")
                for chapter_file in chapter_files:
                    try:
                        chapter_content = chapter_file.read_text(encoding='utf-8')
                        context_parts.append(f"### {chapter_file.stem}\n\n")
                        context_parts.append(chapter_content)
                        context_parts.append("\n")
                    except Exception as e:
                        print(f"[Agent Manager] Error loading {chapter_file.name}: {e}")

        # Load existing scenes
        scenes_dir = self.current_project_dir / "manuscript" / "scenes"
        if scenes_dir.exists():
            scene_files = sorted(scenes_dir.glob("*.md"))
            if scene_files:
                context_parts.append("\n## Existing Scenes\n\n")
                for scene_file in scene_files:
                    try:
                        scene_content = scene_file.read_text(encoding='utf-8')
                        context_parts.append(f"### {scene_file.stem}\n\n")
                        context_parts.append(scene_content)
                        context_parts.append("\n")
                    except Exception as e:
                        print(f"[Agent Manager] Error loading {scene_file.name}: {e}")

        # Load research files
        research_dir = self.current_project_dir / "research"
        if research_dir.exists():
            research_files = sorted(research_dir.glob("*.md"))
            if research_files:
                context_parts.append("\n## Research Notes\n\n")
                for research_file in research_files:
                    try:
                        research_content = research_file.read_text(encoding='utf-8')
                        context_parts.append(f"### {research_file.stem}\n\n")
                        context_parts.append(research_content)
                        context_parts.append("\n")
                    except Exception as e:
                        print(f"[Agent Manager] Error loading {research_file.name}: {e}")

        return ''.join(context_parts)

    def load_agent_instructions(self, agent_num: str) -> Optional[str]:
        """Load instructions for a specific agent"""
        agent_info = self.AGENTS.get(agent_num)
        if not agent_info:
            return None

        agent_file = self.agents_dir / agent_info["file"]
        if not agent_file.exists():
            return None

        return agent_file.read_text(encoding='utf-8')

    def get_agent_name(self, agent_num: str) -> str:
        """Get the name of an agent"""
        return self.AGENTS.get(agent_num, {}).get("name", f"Agent {agent_num}")

    def start_conversation(self, agent_num: str, story_context: Dict) -> None:
        """
        Start a new conversation with an agent

        Args:
            agent_num: Agent number (1-9)
            story_context: Dictionary with story information (idea, themes, etc.)
        """
        self.current_agent = agent_num
        self.conversation_history = []

        # Create a new conversation session file with timestamp
        if self.current_project_dir:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            agent_name = self.get_agent_name(agent_num).lower().replace(" ", "-")

            # Create conversations directory structure
            conversations_dir = self.current_project_dir / "conversations" / f"agent-{agent_num}-{agent_name}"
            conversations_dir.mkdir(parents=True, exist_ok=True)

            self.conversation_session_file = conversations_dir / f"{timestamp}-session.md"

        # Load agent instructions
        instructions = self.load_agent_instructions(agent_num)

        if instructions:
            # Build context message with story information
            context_parts = [
                "# Story Context\n\n",
                f"**Story Idea:** {story_context.get('story_idea', 'Not specified')}\n\n"
            ]

            if story_context.get('themes'):
                context_parts.append(f"**Themes:** {', '.join(story_context.get('themes', []))}\n\n")

            if story_context.get('genre'):
                context_parts.append(f"**Genre:** {story_context.get('genre', 'Literary Fiction')}\n\n")

            if story_context.get('target_word_count'):
                context_parts.append(f"**Target Word Count:** {story_context.get('target_word_count', 80000):,}\n\n")

            # Load all project files (outline, chapters, scenes, story bible, research)
            project_files = self._load_project_files()
            if project_files:
                context_parts.append("\n---\n\n")
                context_parts.append("# Project Files\n\n")
                context_parts.append("Below are all the current files in this novel project. Use this information to maintain consistency and build upon existing work.\n")
                context_parts.append(project_files)

            context = ''.join(context_parts)

            # Add system message with agent instructions
            self.conversation_history.append({
                "role": "system",
                "content": f"{instructions}\n\n{context}"
            })

            # Save conversation start to file
            self._auto_save_conversation()

    def send_message(
        self,
        message: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Send a message to the current agent (async with streaming)

        Args:
            message: User message to send
            on_chunk: Callback for each streamed chunk
            on_complete: Callback when response is complete
            on_error: Callback for errors
        """
        if not self.client:
            if on_error:
                on_error("Claude API not configured. Please set ANTHROPIC_API_KEY environment variable.")
            return

        if not self.current_agent:
            if on_error:
                on_error("No agent selected")
            return

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        # Start generation in background thread
        thread = threading.Thread(
            target=self._generate_response,
            args=(on_chunk, on_complete, on_error)
        )
        thread.daemon = True
        thread.start()

    def _generate_response(
        self,
        on_chunk: Optional[Callable[[str], None]],
        on_complete: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]]
    ) -> None:
        """Generate response from Claude (runs in background thread)"""
        try:
            self.is_generating = True
            self.stop_requested = False

            full_response = ""

            # Prepare messages for API (exclude system messages)
            messages = [
                msg for msg in self.conversation_history
                if msg["role"] != "system"
            ]

            # Get system message
            system_message = next(
                (msg["content"] for msg in self.conversation_history if msg["role"] == "system"),
                None
            )

            # Stream response from Claude
            with self.client.messages.stream(
                model="claude-sonnet-4-5-20250929",
                max_tokens=8192,
                system=system_message,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    if self.stop_requested:
                        break

                    full_response += text

                    if on_chunk:
                        on_chunk(text)

            if not self.stop_requested:
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })

                # Auto-save the conversation after each exchange
                self._auto_save_conversation()
                self._append_to_full_transcript()

                if on_complete:
                    on_complete(full_response)

        except Exception as e:
            if on_error:
                on_error(f"Error generating response: {str(e)}")

        finally:
            self.is_generating = False

    def stop_generation(self) -> None:
        """Stop the current generation"""
        self.stop_requested = True

    def get_conversation_history(self) -> List[Dict]:
        """Get the current conversation history"""
        return self.conversation_history

    def clear_conversation(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
        self.current_agent = None

    def is_api_configured(self) -> bool:
        """Check if Claude API is configured"""
        # Always check current environment for API key
        # (in case it was added after initialization)
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

        if api_key and len(api_key) > 50 and api_key.startswith('sk-ant-'):
            # Valid key exists - reinitialize client if needed
            if not self.client and ANTHROPIC_AVAILABLE:
                try:
                    self.client = Anthropic(api_key=api_key)
                    print(f"[Agent Manager] Initialized client with API key (length: {len(api_key)})")
                except Exception as e:
                    print(f"[Agent Manager] Failed to initialize client: {e}")
                    return False
            return True
        else:
            print(f"[Agent Manager] No valid API key found in environment")
            print(f"[Agent Manager] ANTHROPIC_API_KEY in env: {'ANTHROPIC_API_KEY' in os.environ}")
            if 'ANTHROPIC_API_KEY' in os.environ:
                key_val = os.environ.get('ANTHROPIC_API_KEY', '')
                print(f"[Agent Manager] Key length: {len(key_val)}, starts with sk-ant: {key_val.startswith('sk-ant-') if key_val else False}")
            return False

    def get_last_agent_response(self) -> Optional[str]:
        """Get the last response from the agent"""
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                return msg["content"]
        return None

    def _auto_save_conversation(self):
        """Auto-save the current conversation to the session file"""
        if not self.conversation_session_file or not self.current_project_dir:
            return

        try:
            from datetime import datetime

            # Build conversation content in markdown format
            content = []
            content.append(f"# Conversation with {self.get_agent_name(self.current_agent)}\n")
            content.append(f"**Session Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            content.append("---\n\n")

            for msg in self.conversation_history:
                if msg["role"] == "system":
                    content.append("## System Context\n\n")
                    content.append(f"{msg['content']}\n\n")
                    content.append("---\n\n")
                elif msg["role"] == "user":
                    content.append("### You:\n\n")
                    content.append(f"{msg['content']}\n\n")
                elif msg["role"] == "assistant":
                    content.append(f"### {self.get_agent_name(self.current_agent)}:\n\n")
                    content.append(f"{msg['content']}\n\n")
                    content.append("---\n\n")

            # Write to session file with UTF-8 encoding
            self.conversation_session_file.write_text(''.join(content), encoding='utf-8')

        except Exception as e:
            print(f"[Agent Manager] Error auto-saving conversation: {e}")

    def _append_to_full_transcript(self):
        """Append the latest exchange to the full transcript file"""
        if not self.current_project_dir or not self.conversation_history:
            return

        try:
            from datetime import datetime

            # Full transcript file
            transcript_file = self.current_project_dir / "conversations" / "full-transcript.md"
            transcript_file.parent.mkdir(parents=True, exist_ok=True)

            # Get the last user message and assistant response
            last_messages = []
            for msg in reversed(self.conversation_history):
                if msg["role"] in ["user", "assistant"]:
                    last_messages.insert(0, msg)
                    if len(last_messages) >= 2:
                        break

            if not last_messages:
                return

            # Build transcript entry
            entry = []
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if not transcript_file.exists():
                entry.append("# Full Conversation Transcript\n\n")
                entry.append("Complete history of all agent conversations.\n\n")
                entry.append("---\n\n")

            entry.append(f"## [{timestamp}] {self.get_agent_name(self.current_agent)}\n\n")

            for msg in last_messages:
                if msg["role"] == "user":
                    entry.append("**You:**\n\n")
                    entry.append(f"{msg['content']}\n\n")
                elif msg["role"] == "assistant":
                    entry.append(f"**{self.get_agent_name(self.current_agent)}:**\n\n")
                    entry.append(f"{msg['content']}\n\n")

            entry.append("---\n\n")

            # Append to transcript with UTF-8 encoding
            with open(transcript_file, 'a', encoding='utf-8') as f:
                f.write(''.join(entry))

        except Exception as e:
            print(f"[Agent Manager] Error appending to transcript: {e}")
