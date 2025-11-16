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
        self._cleanup_invalid_keys()

    def _ensure_app_dir(self):
        """Ensure application directory exists"""
        self.app_dir.mkdir(parents=True, exist_ok=True)

    def _cleanup_invalid_keys(self):
        """Remove any invalid API keys from .env file"""
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    content = f.read()

                # Check if there's an API key line
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        # If the key is invalid, remove the file
                        if not self._is_valid_api_key(api_key):
                            self.env_file.unlink()
                            # Also clear from environment if set
                            if "ANTHROPIC_API_KEY" in os.environ:
                                # Only clear if it's the invalid one
                                if os.environ.get("ANTHROPIC_API_KEY", "").strip() == api_key:
                                    del os.environ["ANTHROPIC_API_KEY"]
                            break
            except Exception as e:
                # If we can't read it, it's probably corrupted - remove it
                try:
                    self.env_file.unlink()
                except:
                    pass

    def get_api_key(self) -> Optional[str]:
        """
        Get API key from environment or .env file

        Returns:
            API key if found and valid, None otherwise
        """
        # First check environment variable
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if api_key and self._is_valid_api_key(api_key):
            return api_key

        # Then check .env file
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ANTHROPIC_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if api_key and self._is_valid_api_key(api_key):
                                # Set it in environment for this session
                                os.environ["ANTHROPIC_API_KEY"] = api_key
                                return api_key
            except Exception as e:
                print(f"Error reading .env file: {e}")

        return None

    def _is_valid_api_key(self, api_key: str) -> bool:
        """
        Validate API key format

        Args:
            api_key: The API key to validate

        Returns:
            True if key appears valid, False otherwise
        """
        if not api_key:
            return False

        # Remove whitespace
        api_key = api_key.strip()

        # Check minimum length (Anthropic keys are typically 100+ characters)
        # Being very strict here - real keys are much longer
        if len(api_key) < 50:
            return False

        # Anthropic keys start with specific prefixes
        # Check if it starts with sk-ant- (standard format)
        if not api_key.startswith('sk-ant-'):
            return False

        # Check if it looks like it could be a valid key (has some basic structure)
        # Most API keys are alphanumeric with dashes/underscores
        if not any(c.isalnum() for c in api_key):
            return False

        return True

    def save_api_key(self, api_key: str) -> Tuple[bool, str]:
        """
        Save API key to .env file

        Args:
            api_key: The API key to save

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate key format
            api_key = api_key.strip()

            if not self._is_valid_api_key(api_key):
                return False, "API key appears to be invalid.\n\nPlease check that you copied the full key from Anthropic."

            # Save to .env file
            with open(self.env_file, 'w') as f:
                f.write(f"ANTHROPIC_API_KEY={api_key}\n")

            # Set in current environment
            os.environ["ANTHROPIC_API_KEY"] = api_key

            # Make file readable only by user (chmod 600)
            os.chmod(self.env_file, 0o600)

            return True, f"API key saved successfully!"

        except Exception as e:
            return False, f"Error saving API key: {str(e)}"

    def is_configured(self) -> bool:
        """Check if API key is configured and valid"""
        api_key = self.get_api_key()
        is_valid = api_key is not None and len(api_key) > 0

        # Debug logging (can be removed later)
        if not is_valid:
            print("[API Key Manager] No valid API key found")
            print(f"[API Key Manager] .env file exists: {self.env_file.exists()}")
            print(f"[API Key Manager] Environment variable set: {'ANTHROPIC_API_KEY' in os.environ}")
        else:
            print(f"[API Key Manager] Valid API key found (length: {len(api_key)})")

        return is_valid

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
