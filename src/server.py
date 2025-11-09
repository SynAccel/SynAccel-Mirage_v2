from fastapi import FastAPI, Request
from src.detection import detect_probe
from src.response_engine import send_fake_banner
from src.telemetry import log_event
from src.persona_engine import load_persona
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "SynAccel Mirage v2 operational."}

@app.get("/banner")
async def banner_endpoint(request: Request):
    probe_data = await detect_probe(request)

    # Persona decision logic
    user_agent = probe_data["user_agent"].lower()
    if any(term in user_agent for term in ["nmap", "sqlmap", "dirbuster", "masscan"]):
        persona_name = "scanner"
    elif "mozilla" in user_agent or "chrome" in user_agent:
        persona_name = "opportunist"
    else:
        persona_name = "default"

    persona = load_persona(persona_name)

    # Pick one service type from persona
    service_type = persona["fake_services"][0]
    banner_text = persona["banners"][service_type]

    fake_banner = PlainTextResponse(content=banner_text)

    # Log event
    event = {
        "ip": probe_data["ip"],
        "user_agent": probe_data["user_agent"],
        "suspicious": probe_data["suspicious"],
        "persona": persona_name,
        "banner_sent": banner_text
    }
    await log_event(event)

    print(f"[MIRAGE] {probe_data['ip']} assigned persona '{persona_name}'")
    return fake_banner

