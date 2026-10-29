import json
import logging
import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
PERSONA_DIR = BASE_DIR / "personas"
PERSONA_NAME = re.compile(r"^[a-zA-Z0-9_-]+$")
logger = logging.getLogger(__name__)


def load_persona(name: str = "default") -> dict[str, Any]:
    """
    Load and validate a persona from the repository's personas directory.
    Unknown names fall back to the default persona.
    """
    if not PERSONA_NAME.fullmatch(name):
        logger.warning("Invalid persona name %r; using default persona", name)
        name = "default"

    persona_path = PERSONA_DIR / f"{name}.json"
    if not persona_path.exists():
        logger.warning("Persona %r not found; using default persona", name)
        persona_path = PERSONA_DIR / "default.json"

    try:
        with persona_path.open("r", encoding="utf-8") as persona_file:
            data = json.load(persona_file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to load persona configuration: {persona_path.name}") from error

    if not isinstance(data, dict):
        raise ValueError(f"Persona configuration must be an object: {persona_path.name}")

    services = data.get("fake_services")
    banners = data.get("banners")
    if (
        not isinstance(services, list)
        or not services
        or not all(isinstance(service, str) and service for service in services)
        or not isinstance(banners, dict)
        or any(service not in banners or not isinstance(banners[service], str) for service in services)
    ):
        raise ValueError(f"Persona configuration has invalid services or banners: {persona_path.name}")

    return data
