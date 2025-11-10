# SynAccel Mirage v2  
### Adaptive Deception Framework — Behavioral Honeypot Core

**Mirage v2** is the adaptive brain of the SynAccel Cyber ecosystem.  
It simulates *psychological deception environments* — generating believable fake banners, service responses, and persona-driven worlds that adapt based on attacker behavior.

---

## Current Capabilities (v2 Core)
**Core Systems:**
- **Detection Layer:** Identifies incoming probes, extracts IP and User-Agent data, and flags suspicious scanners.
- **Response Engine:** Generates believable fake banners (SSH, HTTP, FTP, SMTP) for each request.
- **Telemetry System:** Records every interaction to structured logs (`logs/perception_log.jsonl`) for behavioral analysis.
- **Persona Engine:** Loads configurable “personas” from JSON templates (default, opportunist, scanner) and serves matching illusions.
- **Automatic Persona Assignment:** Detects reconnaissance tools (e.g., nmap, sqlmap) and responds with tailored persona environments.

---

## Project Vision
**Goal:**  
Transform Mirage from a static honeypot into an *adaptive organism* — a system that:
- Evolves deception dynamically per attacker.
- Generates unique “worlds” per IP or behavior profile.
- Can eventually integrate with **SynAccel Bridge** for real multi-port, network-level illusions.


---

## Architecture Concept

```
           ┌───────────────────────────┐
           │        Internet           │
           └────────────┬──────────────┘
                        │
                ┌───────▼────────┐
                │ SYNACCEL MIRAGE│
                │  (reverse proxy)│
                ├────────────────┤
                │ Detection Layer│──► Logs & Persona IDs
                │ Persona Engine │──► Generates fake world
                │ Response Layer │──► Serves illusions
                │ Telemetry Core │──► Perception Map (JSONL)
                └───────┬────────┘
                        │
                  ┌─────▼──────┐
                  │ Real System│  (never exposed)
                  └────────────┘
```


---

##  Early Prototype Ideas

- [ ] Detect basic nmap scans via timing and headers.  
- [ ] Serve unique fake service banners per attacker.  
- [ ] Generate decoy HTML login pages dynamically.  
- [ ] Log all requests to a `perception_log.jsonl`.  
  
---

##  Vision

> *Security is no longer just defense. It’s deception with purpose.*

SynAccel Mirage v2 is part of a broader SynAccel Cyber initiative exploring adaptive security loops, AI-assisted defense, and cognitive misdirection.

This repository is a research playground — not a product — for experimenting with perception as a defensive surface.

---

## Usage

```
uvicorn src.server:app --reload
```

**Status:** Concept Prototype (R&D)  
**License:** MIT  
**Author:** [Nicholas J. D’Acri — ClearLotus / SynAccel Cyber]



_Local sync test: working on prototype phase_



















