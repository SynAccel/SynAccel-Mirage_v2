# SynAccel Mirage v2  
### Adaptive Cognitive Deception for Real-Time Misdirection  

**SynAccel Mirage v2** is an experimental deception framework that builds *personalized illusions* for every attacker.  
Instead of blocking scans, Mirage listens, learns, and reflects a fake reality that evolves with the intruder’s behavior.

---

## Concept

When a probe or scan hits your system, Mirage acts as a **behavioral mirror**:

1. **Detects** reconnaissance patterns (e.g., nmap, dirbuster, burp).  
2. **Profiles** the intruder’s style and assigns them a unique persona.  
3. **Generates** a believable decoy environment — fake ports, banners, credentials, and data trails.  
4. **Responds** dynamically so that each attacker experiences a different “truth.”  
5. **Logs** their perceived world, turning psychology into telemetry.

Mirage is less about *hiding* and more about *storytelling* — crafting a world convincing enough that an attacker gets lost inside it.

---

## Why It Matters

Traditional honeypots show the same façade to everyone.  
**Mirage learns who’s looking and rewrites reality accordingly.**  

It bridges cybersecurity, behavioral science, and adaptive AI — exploring how machines can *shape attacker perception* in real time.

---

## Core Components

| Layer | Purpose |
|-------|----------|
| Detection | Identify probes, scans, or suspicious traffic patterns. |
| Persona Engine | Build individualized decoy worlds using JSON templates and generative text. |
| Response Layer | Serve dynamic banners, pages, and files without exposing the real system. |
| Telemetry Core | Log what attackers *believe* exists (their “perception map”). |
| Adaptive Loop | (Future) Learn which illusions work best and evolve automatically. |

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
- [ ] (Later) Visualize attacker belief map with Streamlit.  

---

##  Vision

> *Security is no longer just defense. It’s deception with purpose.*

SynAccel Mirage v2 is part of a broader SynAccel Cyber initiative exploring adaptive security loops, AI-assisted defense, and cognitive misdirection.

This repository is a research playground — not a product — for experimenting with perception as a defensive surface.

---

**Status:** Concept Prototype (R&D)  
**License:** MIT  
**Author:** [Nicholas J. D’Acri — ClearLotus / SynAccel Cyber]






















