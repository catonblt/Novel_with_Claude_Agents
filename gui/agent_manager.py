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
        self.is_generating = False
        self.stop_requested = False

        # Initialize Anthropic client if available
        if ANTHROPIC_AVAILABLE:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.client = Anthropic(api_key=api_key)

    def load_agent_instructions(self, agent_num: str) -> Optional[str]:
        """Load instructions for a specific agent"""
        agent_info = self.AGENTS.get(agent_num)
        if not agent_info:
            return None

        agent_file = self.agents_dir / agent_info["file"]
        if not agent_file.exists():
            return None

        return agent_file.read_text()

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

        # Load agent instructions
        instructions = self.load_agent_instructions(agent_num)

        if instructions:
            # Build context message with story information
            context_parts = [
                "# Story Context\n",
                f"**Story Idea:** {story_context.get('story_idea', 'Not specified')}\n"
            ]

            if story_context.get('themes'):
                context_parts.append(f"**Themes:** {', '.join(story_context.get('themes', []))}\n")

            if story_context.get('genre'):
                context_parts.append(f"**Genre:** {story_context.get('genre', 'Literary Fiction')}\n")

            if story_context.get('target_word_count'):
                context_parts.append(f"**Target Word Count:** {story_context.get('target_word_count', 80000):,}\n")

            context = ''.join(context_parts)

            # Add system message with agent instructions
            self.conversation_history.append({
                "role": "system",
                "content": f"{instructions}\n\n{context}"
            })

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
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
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
        return self.client is not None

    def get_last_agent_response(self) -> Optional[str]:
        """Get the last response from the agent"""
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                return msg["content"]
        return None
