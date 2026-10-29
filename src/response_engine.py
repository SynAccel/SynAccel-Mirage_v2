import random
from typing import Any


def select_fake_banner(persona: dict[str, Any], service: str | None = None) -> tuple[str, str]:
    """Return a service and its configured banner, choosing randomly by default."""
    services = persona["fake_services"]
    selected_service = service.upper() if service else random.choice(services)
    if selected_service not in services:
        raise ValueError(f"Service is not available for this persona: {selected_service}")
    return selected_service, persona["banners"][selected_service]


def send_fake_banner(banner: str):
    """Build a non-cacheable plain-text decoy response."""
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(
        content=banner,
        headers={
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )