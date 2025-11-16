"""
API Key Management - Handles Anthropic API key setup and storage
"""

import os
from pathlib import Path
from typing import Optional, Tuple


class APIKeyManager:
    """Manages Anthropic API key configuration"""

    def __init__(self, app_dir: Optional[Path] = None):
        """Initialize API key manager"""
        if app_dir:
            self.app_dir = Path(app_dir)
        else:
            # Use home directory for config
            self.app_dir = Path.home() / ".novel_writer"

        self.env_file = self.app_dir / ".env"
        self._ensure_app_dir()

    def _ensure_app_dir(self):
        """Ensure application directory exists"""
        self.app_dir.mkdir(parents=True, exist_ok=True)

    def get_api_key(self) -> Optional[str]:
        """
        Get API key from environment or .env file

        Returns:
            API key if found, None otherwise
        """
        # First check environment variable
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            return api_key

        # Then check .env file
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ANTHROPIC_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if api_key:
                                # Set it in environment for this session
                                os.environ["ANTHROPIC_API_KEY"] = api_key
                                return api_key
            except Exception as e:
                print(f"Error reading .env file: {e}")

        return None

    def save_api_key(self, api_key: str) -> Tuple[bool, str]:
        """
        Save API key to .env file

        Args:
            api_key: The API key to save

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate key format (basic check)
            if not api_key or len(api_key) < 10:
                return False, "API key appears to be invalid (too short)"

            # Save to .env file
            with open(self.env_file, 'w') as f:
                f.write(f"ANTHROPIC_API_KEY={api_key}\n")

            # Set in current environment
            os.environ["ANTHROPIC_API_KEY"] = api_key

            # Make file readable only by user (chmod 600)
            os.chmod(self.env_file, 0o600)

            return True, f"API key saved to {self.env_file}"

        except Exception as e:
            return False, f"Error saving API key: {str(e)}"

    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return self.get_api_key() is not None

    def clear_api_key(self) -> Tuple[bool, str]:
        """
        Clear the saved API key

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if self.env_file.exists():
                self.env_file.unlink()

            # Clear from environment
            if "ANTHROPIC_API_KEY" in os.environ:
                del os.environ["ANTHROPIC_API_KEY"]

            return True, "API key cleared"

        except Exception as e:
            return False, f"Error clearing API key: {str(e)}"
