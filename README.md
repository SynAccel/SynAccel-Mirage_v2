# SynAccel Mirage

Mirage is a small defensive decoy service. It classifies requests using broad
User-Agent signals, returns a configured plain-text service banner, and appends
interaction metadata to a JSON Lines log. It does not proxy to or connect to a
real service.

---

## Current Capabilities

- Classifies broad User-Agent signals into scanner, researcher, browser-like, or default profiles.
- Returns a configured plain-text banner, randomly choosing among the selected persona's services unless `service` is provided.
- Logs JSON Lines events with a UTC timestamp; the log path can be set with `MIRAGE_LOG_FILE`.
- Exposes `/`, `/healthz`, and `/banner` endpoints.
- Keeps all responses local; it does not forward requests to another service.

---

## Project Vision
**Goal:**  
Transform Mirage from a static honeypot into an *adaptive organism* — a system that:
- Evolves deception dynamically per attacker.
- Generates unique “worlds” per IP or behavior profile.
- Can eventually integrate with **SynAccel Bridge** for real multi-port, network-level illusions.


---

## Request Flow

`GET /banner` -> request metadata -> persona profile -> selected text banner
-> JSON Lines telemetry. Requests are not forwarded to an upstream service.


---

## Run

Install the pinned dependencies and start the API from the repository root:

```bash
python -m pip install -r requirements.txt
uvicorn src.server:app --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`. `GET /` reports service
metadata, `GET /healthz` is a lightweight health check, and `GET /banner`
returns a selected banner as plain text. An optional `service` query parameter
selects a service offered by the automatically chosen persona, for example
`GET /banner?service=SSH`. Unsupported services return `404`.

---

##  Vision

> *Security is no longer just defense. It’s deception with purpose.*

SynAccel Mirage v2 is part of a broader SynAccel Cyber initiative exploring adaptive security loops, AI-assisted defense, and cognitive misdirection.

This repository is a research playground — not a product — for experimenting with perception as a defensive surface.

---

## Personas and Telemetry

Persona JSON files live in `personas/`. A persona must provide a non-empty
`fake_services` list and a string banner for each listed service. Scanner and
research tooling markers select the `scanner` and `researcher` personas;
browser-like agents select `opportunist`, and other requests use `default`.
The `targeted` profile is not automatically assigned. User-Agent values are
untrusted hints, not identity or reliable evidence of intent.

Events are appended to `logs/perception_log.jsonl`; parent directories are
created automatically. Set `MIRAGE_LOG_FILE` to change the destination. Each
record includes the source address when available, a bounded User-Agent,
classification, chosen service, response banner, and a UTC timestamp.

Run the focused checks with:

```bash
python -m unittest discover -s tests -v
```

**Status:** Concept Prototype (R&D)  
**Author:** [Nicholas J. D’Acri — ClearLotus / SynAccel Cyber]

Before deployment, restrict network exposure, protect and rotate telemetry, and
review privacy and retention requirements. Do not trust forwarded client-IP
headers unless a trusted proxy is explicitly configured. This prototype has not
been hardened or load-tested for production use.



















