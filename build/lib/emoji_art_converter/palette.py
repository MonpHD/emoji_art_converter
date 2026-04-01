import json
import os
from pathlib import Path

def _get_data_path():
    """Pfad zur data/emoji_palette.json ermitteln."""
    return Path(__file__).parent / "data" / "emoji_palette.json"

def load_palette():
    """Lädt die Emoji-Palette aus der JSON-Datei."""
    with open(_get_data_path(), "r", encoding="utf-8") as f:
        return json.load(f)