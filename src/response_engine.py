from fastapi.responses import PlainTextResponse
import random

# a simple list of service banners
FAKE_BANNERS = [
     "SSH-2.0-OpenSSH_8.4p1 Debian-5",
    "220 ProFTPD 1.3.5a Server ready.",
    "HTTP/1.1 200 OK\nServer: Apache/2.4.51 (Ubuntu)\nContent-Type: text/html; charset=UTF-8",
    "220 Microsoft ESMTP MAIL Service ready at Tue, 9 Nov 2025 12:00:00 -0500"
]

def generate_fake_banner():
    """Pick a random banner from list to act as Mirage's illusion"""
    return random.choice(FAKE_BANNERS)

async def send_fake_banner():
    banner = generate_fake_banner()
    return PlainTextResponse(content=banner)