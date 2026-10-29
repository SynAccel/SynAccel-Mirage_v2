import logging

from fastapi import FastAPI, HTTPException, Request

from src.detection import detect_probe, select_persona
from src.persona_engine import load_persona
from src.response_engine import select_fake_banner, send_fake_banner
from src.telemetry import log_event

logger = logging.getLogger(__name__)
app = FastAPI(title="SynAccel Mirage", version="2.1.0")


@app.get("/")
async def home():
    return {"name": "SynAccel Mirage", "status": "operational", "version": app.version}


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


@app.get("/banner")
async def banner_endpoint(request: Request, service: str | None = None):
    probe_data = await detect_probe(request)
    persona_name = select_persona(probe_data["user_agent"])
    persona = load_persona(persona_name)
    try:
        service_type, banner_text = select_fake_banner(persona, service)
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Service is not available for this persona") from error

    event = {
        "ip": probe_data["ip"],
        "user_agent": probe_data["user_agent"],
        "suspicious": probe_data["suspicious"],
        "persona": persona_name,
        "service": service_type,
        "banner_sent": banner_text
    }
    try:
        await log_event(event)
    except OSError:
        logger.exception("Unable to persist interaction telemetry")

    logger.info("Assigned persona %s and service %s", persona_name, service_type)
    return send_fake_banner(banner_text)

