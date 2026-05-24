# ── data.py ───────────────────────────────────────────────────────────────────
# Handles all reading and writing of card data to disk.
# Data format: { "deck_name": [ {"front": "...", "back": "..."}, ... ] }

import json
import os
from constants import DATA_FILE


def load_data() -> dict:
    """Load all decks from the local JSON file. Returns an empty dict if none exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data: dict) -> None:
    """Persist all decks to the local JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
