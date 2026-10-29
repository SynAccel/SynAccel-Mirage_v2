from fastapi import Request

SCANNER_MARKERS = ("nmap", "sqlmap", "dirbuster", "masscan", "nikto", "nuclei")
SCRIPT_MARKERS = SCANNER_MARKERS + ("curl", "wget", "python-requests", "httpx")
RESEARCHER_MARKERS = ("burp", "zaproxy", "owasp zap")


async def detect_probe(request: Request):
    """Collect bounded request metadata and flag recognizable automation."""
    client = request.client
    attacker_ip = client.host if client is not None else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")[:512]
    suspicious = any(marker in user_agent.lower() for marker in SCRIPT_MARKERS)

    return {
        "ip": attacker_ip,
        "user_agent": user_agent,
        "suspicious": suspicious
    }


def select_persona(user_agent: str) -> str:
    """Choose a response profile from broad User-Agent signals."""
    normalized = user_agent.lower()
    if any(marker in normalized for marker in SCANNER_MARKERS):
        return "scanner"
    if any(marker in normalized for marker in RESEARCHER_MARKERS):
        return "researcher"
    if "mozilla" in normalized or "chrome" in normalized:
        return "opportunist"
    return "default"