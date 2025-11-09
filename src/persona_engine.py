import json
from pathlib import Path
from typing import Dict

PERSONA_DIR = Path("personas")

def load_persona(name: str = "default") -> Dict:
    """
    Load a persona file from the personas/ directory.
    If not found, fallback to 'default.json'.
    """
    persona_path = PERSONA_DIR / f"{name}.json"

    if not persona_path.exists():
        print(f"[MIRAGE] Persona '{name}' not found. Using default persona.")
        persona_path = PERSONA_DIR / "default.json"

    with open(persona_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
