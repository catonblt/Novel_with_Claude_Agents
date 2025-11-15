"""
Utility functions for the Novel Writing GUI
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional


def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def format_timestamp() -> str:
    """Get current timestamp in standard format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if not"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def word_count(text: str) -> int:
    """Count words in text"""
    return len(text.split())
