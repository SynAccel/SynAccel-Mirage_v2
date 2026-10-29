import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException
from starlette.requests import Request

from src import telemetry
from src.detection import detect_probe, select_persona
from src.persona_engine import PERSONA_DIR, load_persona
from src.response_engine import select_fake_banner, send_fake_banner
from src.server import banner_endpoint


def make_request(user_agent: str | None = None, client: tuple[str, int] | None = ("127.0.0.1", 1234)) -> Request:
    headers = []
    if user_agent is not None:
        headers.append((b"user-agent", user_agent.encode()))
    return Request({"type": "http", "headers": headers, "client": client, "method": "GET", "path": "/banner"})


class DetectionTests(unittest.TestCase):
    def test_selects_persona_from_user_agent(self):
        self.assertEqual(select_persona("nmap/7.9"), "scanner")
        self.assertEqual(select_persona("Burp Suite"), "researcher")
        self.assertEqual(select_persona("Mozilla/5.0 Chrome/120"), "opportunist")
        self.assertEqual(select_persona("unknown"), "default")

    def test_missing_client_and_oversized_user_agent_are_safe(self):
        probe = asyncio.run(detect_probe(make_request("x" * 600, client=None)))
        self.assertEqual(probe["ip"], "unknown")
        self.assertEqual(len(probe["user_agent"]), 512)


class PersonaTests(unittest.TestCase):
    def test_all_personas_have_valid_service_banners(self):
        for path in PERSONA_DIR.glob("*.json"):
            with self.subTest(persona=path.stem):
                persona = load_persona(path.stem)
                self.assertTrue(persona["fake_services"])

    def test_unknown_and_path_like_names_fall_back_to_default(self):
        self.assertEqual(load_persona("does-not-exist")["name"], "default")
        self.assertEqual(load_persona("../default")["name"], "default")


class ResponseTests(unittest.TestCase):
    def test_service_selection_is_validated_and_case_insensitive(self):
        persona = load_persona("default")
        self.assertEqual(select_fake_banner(persona, "ssh")[0], "SSH")
        with self.assertRaises(ValueError):
            select_fake_banner(persona, "SMTP")

    def test_response_is_non_cacheable_plain_text(self):
        response = send_fake_banner("SSH-2.0-test")
        self.assertEqual(response.body, b"SSH-2.0-test")
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")

    def test_endpoint_logs_selected_persona_and_service(self):
        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / "nested" / "events.jsonl"
            with patch.object(telemetry, "LOG_FILE", log_path):
                response = asyncio.run(banner_endpoint(make_request("nmap"), service="FTP"))
            self.assertIn(b"ProFTPD", response.body)
            event = json.loads(log_path.read_text(encoding="utf-8"))
            self.assertEqual(event["persona"], "scanner")
            self.assertEqual(event["service"], "FTP")
            self.assertTrue(event["suspicious"])
            self.assertTrue(event["timestamp"].endswith("+00:00"))

    def test_endpoint_rejects_services_not_offered_by_persona(self):
        with self.assertRaises(HTTPException) as error:
            asyncio.run(banner_endpoint(make_request("Mozilla/5.0 Chrome/120"), service="SSH"))
        self.assertEqual(error.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()