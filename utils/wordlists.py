import os
from config import Config

class WordlistManager:
    """Manage wordlist paths and loading."""

    def get_path(self, name: str) -> str:
        """Return path for a named wordlist, or empty string if not found."""
        path = Config.WORDLISTS.get(name, "")
        if path and os.path.exists(path):
            return path
        return ""

    def load(self, name: str) -> list:
        """Load a wordlist by name, returning a list of words."""
        path = self.get_path(name)
        if not path:
            return []
        try:
            with open(path, 'r', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    def available(self) -> list:
        """Return names of available (existing) wordlists."""
        return [name for name, path in Config.WORDLISTS.items() if os.path.exists(path)]
