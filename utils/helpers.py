import os
import json

class Color:
    """ANSI color codes for pretty output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'


def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def save_json(data: dict, filepath: str):
    """Save a dict as a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath: str) -> dict:
    """Load a JSON file into a dict."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename."""
    return name.replace('/', '_').replace('\\', '_').replace(':', '_')

def file_size(filepath: str) -> int:
    """Return file size in bytes, 0 if not found."""
    try:
        return os.path.getsize(filepath)
    except:
        return 0
