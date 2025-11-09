from fastapi import Request

# radar
async def detect_probe(request: Request):
    """Detect scanning or suspicious behavior based on request headers or patterns.
    Now, capturing basic info about who is connected."""
    attacker_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "unknown")
    
    # Simple check: if user agent looks like a scanner or script
    
    suspicious = any(keyword in user_agent.lower() for keyword in ["nmap", "sqlmap", "dirbuster", "curl"])
    
    # Return structured data
    return {
        "ip": attacker_ip,
        "user_agent": user_agent,
        "suspicious": suspicious
    }