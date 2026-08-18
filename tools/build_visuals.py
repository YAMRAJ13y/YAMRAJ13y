"""Generate the self-hosted animated SVGs used by the profile README.

Everything is emitted into assets/ with the artwork inlined as base64, so the
visuals render straight from raw.githubusercontent with no third-party widget
service in the path.

Usage:  python tools/build_visuals.py
"""

import base64
import io
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_LOGO = os.path.join(ROOT, "yamraj logo.png")
ASSETS = os.path.join(ROOT, "assets")

# Bounding box of the emblem inside the source artwork (detected by saturation).
EMBLEM_BOX = (389, 55, 1149, 815)

CYAN = "#00F0FF"
RED = "#FF003C"
GREEN = "#39FF14"
MUTED = "#8B949E"
BG = "#05070d"


def emblem_data_uri(size=200, quality=78):
    im = Image.open(SRC_LOGO).convert("RGB").crop(EMBLEM_BOX)
    buf = io.BytesIO()
    im.resize((size, size), Image.LANCZOS).save(
        buf, "JPEG", quality=quality, optimize=True
    )
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build_hero():
    """Animated header: emblem, rotating sigil rings, neon wordmark, typed tagline."""
    W, H = 1200, 340
    cx, cy, r = 170, 170, 100  # emblem centre / radius
    uri = emblem_data_uri()

    # Twinkling particles: (x, y, radius, delay)
    parts = [
        (430, 58, 1.8, 0.0), (520, 292, 1.4, 1.1), (700, 44, 1.6, 2.2),
        (880, 300, 1.9, 0.6), (1010, 70, 1.5, 1.7), (1120, 250, 1.7, 2.8),
        (620, 316, 1.3, 3.3), (960, 36, 1.4, 0.9), (350, 300, 1.5, 2.5),
        (1150, 130, 1.6, 1.4), (480, 150, 1.2, 3.0), (1080, 190, 1.3, 2.0),
    ]
    particles = "\n".join(
        f'<circle class="tw" cx="{x}" cy="{y}" r="{rr}" fill="{CYAN}" '
        f'style="animation-delay:{d}s"/>'
        for x, y, rr, d in parts
    )

    # Perspective floor lines
    floor = "\n".join(
        f'<line x1="{330 + i * 62}" y1="340" x2="{250 + i * 96}" y2="272" '
        f'stroke="{CYAN}" stroke-width="1" opacity="0.10"/>'
        for i in range(14)
    )

    tagline = "Full-Stack Developer  //  AI-Security Engineer  //  Red Teamer"
    subline = "7 open-source security engines  ·  one platform"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="YAMRAJ 13 - Solanki Sumit">
<title>YAMRAJ 13 // Solanki Sumit</title>
<defs>
  <linearGradient id="wordmark" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{CYAN}"/>
    <stop offset="55%" stop-color="#8A7BFF"/>
    <stop offset="100%" stop-color="{RED}"/>
  </linearGradient>
  <radialGradient id="vignette" cx="50%" cy="45%" r="72%">
    <stop offset="0%" stop-color="#0d1524"/>
    <stop offset="100%" stop-color="{BG}"/>
  </radialGradient>
  <radialGradient id="emblemFade" cx="50%" cy="50%" r="50%">
    <stop offset="72%" stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="softCircle">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#emblemFade)"/>
  </mask>
  <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{CYAN}" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{CYAN}"/>
    <stop offset="50%" stop-color="{RED}"/>
    <stop offset="100%" stop-color="{GREEN}"/>
  </linearGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="typeClip">
    <rect x="352" y="176" width="0" height="30">
      <animate attributeName="width" values="0;540;540;540" keyTimes="0;0.42;0.92;1"
               dur="7s" repeatCount="indefinite" calcMode="spline"
               keySplines="0.2 0 0.1 1;0 0 1 1;0 0 1 1"/>
    </rect>
  </clipPath>
</defs>

<style>
  .tw {{ animation: tw 3.6s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:.9 }} }}
  .ring1 {{ transform-origin:{cx}px {cy}px; animation: spin 22s linear infinite; }}
  .ring2 {{ transform-origin:{cx}px {cy}px; animation: spin 34s linear infinite reverse; }}
  @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  .halo {{ transform-origin:{cx}px {cy}px; animation: breathe 4.5s ease-in-out infinite; }}
  @keyframes breathe {{ 0%,100% {{ opacity:.25; transform:scale(1) }} 50% {{ opacity:.6; transform:scale(1.04) }} }}
  .word {{ animation: flick 6s ease-in-out infinite; }}
  @keyframes flick {{ 0%,100% {{ opacity:1 }} 47% {{ opacity:1 }} 49% {{ opacity:.72 }} 51% {{ opacity:1 }} }}
  .scan {{ animation: scan 5.5s linear infinite; }}
  @keyframes scan {{ 0% {{ transform:translateY(-14px) }} 100% {{ transform:translateY(354px) }} }}
  .cursor {{ animation: blink 1.05s steps(1) infinite; }}
  @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
  .dot {{ animation: tw 2.4s ease-in-out infinite; }}
  @media (prefers-reduced-motion: reduce) {{
    .tw,.ring1,.ring2,.halo,.word,.scan,.cursor,.dot {{ animation: none }}
  }}
</style>

<rect width="{W}" height="{H}" fill="url(#vignette)"/>
{floor}
{particles}

<!-- emblem + sigil rings -->
<circle class="halo" cx="{cx}" cy="{cy}" r="{r + 16}" fill="{CYAN}" opacity="0.25" filter="url(#glow)"/>
<image href="{uri}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" mask="url(#softCircle)"/>
<g class="ring1" fill="none" stroke="{CYAN}" stroke-width="1.1" opacity="0.55">
  <circle cx="{cx}" cy="{cy}" r="{r + 14}" stroke-dasharray="3 9"/>
  <circle cx="{cx}" cy="{cy}" r="{r + 26}" stroke-dasharray="26 150" opacity="0.75"/>
</g>
<g class="ring2" fill="none" stroke="{RED}" stroke-width="1" opacity="0.4">
  <circle cx="{cx}" cy="{cy}" r="{r + 21}" stroke-dasharray="1 15"/>
</g>

<!-- wordmark -->
<text class="word" x="352" y="132" font-family="'Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
      font-size="72" font-weight="700" letter-spacing="7" fill="url(#wordmark)" filter="url(#glow)">YAMRAJ 13</text>

<!-- typed tagline -->
<g clip-path="url(#typeClip)">
  <text x="352" y="198" font-family="'Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
        font-size="17.5" letter-spacing="0.6" fill="{MUTED}">{tagline}</text>
</g>
<rect class="cursor" x="352" y="180" width="9" height="20" fill="{GREEN}" opacity="0.85">
  <animate attributeName="x" values="352;892;892;892" keyTimes="0;0.42;0.92;1" dur="7s"
           repeatCount="indefinite" calcMode="spline" keySplines="0.2 0 0.1 1;0 0 1 1;0 0 1 1"/>
</rect>

<!-- status line -->
<circle class="dot" cx="358" cy="240" r="4" fill="{GREEN}"/>
<text x="374" y="245" font-family="'Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
      font-size="14.5" fill="{GREEN}" opacity="0.92">{subline}</text>

<rect x="352" y="272" width="700" height="2" fill="url(#rule)" opacity="0.75"/>

<!-- HUD ticks -->
<g stroke="{CYAN}" stroke-width="1.4" opacity="0.5" fill="none">
  <path d="M24 24 h34 M24 24 v34"/>
  <path d="M{W - 24} 24 h-34 M{W - 24} 24 v34"/>
  <path d="M24 {H - 24} h34 M24 {H - 24} v-34"/>
  <path d="M{W - 24} {H - 24} h-34 M{W - 24} {H - 24} v-34"/>
</g>

<rect class="scan" x="0" y="0" width="{W}" height="14" fill="url(#sweep)" opacity="0.30"/>
</svg>
"""


def build_divider():
    """Thin animated rule that replaces the capsule-render dividers."""
    W = 1200
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="4" viewBox="0 0 {W} 4" role="presentation">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{CYAN}"/><stop offset="50%" stop-color="{RED}"/>
    <stop offset="100%" stop-color="{GREEN}"/>
  </linearGradient>
  <linearGradient id="pulse" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
    <stop offset="50%" stop-color="#fff" stop-opacity="0.85"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  .p {{ animation: slide 6s linear infinite; }}
  @keyframes slide {{ 0% {{ transform:translateX(-260px) }} 100% {{ transform:translateX({W}px) }} }}
  @media (prefers-reduced-motion: reduce) {{ .p {{ animation:none; opacity:0 }} }}
</style>
<rect width="{W}" height="4" rx="2" fill="url(#g)" opacity="0.85"/>
<rect class="p" x="0" y="0" width="260" height="4" rx="2" fill="url(#pulse)" opacity="0.7"/>
</svg>
"""


def build_engines():
    """Status-board panel listing the seven security engines with live-looking dots."""
    rows = [
        ("EchoTrap", "prompt-injection lab + defense", "OWASP LLM01", CYAN),
        ("SkillSentry", "malicious MCP / agent-skill scanner", "OWASP AGENTIC", GREEN),
        ("PatchPilot", "KEV + EPSS exploit-first patching", "VULN MGMT", CYAN),
        ("IOCForge", "multi-feed IOC enrichment &amp; triage", "SOC TRIAGE", GREEN),
        ("IdentityWatch", "detection-as-code for identity attacks", "MITRE ATT&amp;CK", CYAN),
        ("PickleGuard", "malicious pickle opcodes in ML models", "ML SUPPLY CHAIN", GREEN),
        ("LeakLens", "ransomware leak-site intelligence", "CTI / OSINT", CYAN),
    ]
    W = 1200
    top = 78
    step = 46
    H = top + step * len(rows) + 26

    body = []
    for i, (name, desc, tag, colour) in enumerate(rows):
        y = top + i * step
        body.append(f"""
<g>
  <rect x="26" y="{y - 26}" width="{W - 52}" height="38" rx="6" fill="#0D1117" opacity="0.55"/>
  <circle class="dot" cx="52" cy="{y - 7}" r="5" fill="{colour}" style="animation-delay:{i * 0.32:.2f}s"/>
  <text x="74" y="{y - 2}" font-family="'Fira Code',ui-monospace,Consolas,monospace" font-size="16"
        font-weight="700" fill="#e6edf3">{name}</text>
  <text x="248" y="{y - 2}" font-family="'Fira Code',ui-monospace,Consolas,monospace" font-size="14"
        fill="{MUTED}">{desc}</text>
  <text x="{W - 46}" y="{y - 2}" text-anchor="end" font-family="'Fira Code',ui-monospace,Consolas,monospace"
        font-size="12" letter-spacing="1.2" fill="{colour}" opacity="0.85">{tag}</text>
</g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Security Lab engine status board">
<title>Security_Lab // seven engines</title>
<defs>
  <linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{GREEN}"/>
  </linearGradient>
</defs>
<style>
  .dot {{ animation: pulse 2.6s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity:.28 }} 50% {{ opacity:1 }} }}
  @media (prefers-reduced-motion: reduce) {{ .dot {{ animation:none; opacity:.9 }} }}
</style>
<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="none" stroke="{CYAN}" stroke-width="1" opacity="0.28"/>
<text x="30" y="42" font-family="'Fira Code',ui-monospace,Consolas,monospace" font-size="19" font-weight="700"
      fill="url(#hdr)">SECURITY_LAB</text>
<text x="{W - 30}" y="42" text-anchor="end" font-family="'Fira Code',ui-monospace,Consolas,monospace"
      font-size="13" fill="{MUTED}">7 engines &#183; 1 platform &#183; MIT</text>
<rect x="30" y="54" width="{W - 60}" height="1" fill="{CYAN}" opacity="0.25"/>
{''.join(body)}
</svg>
"""


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for name, svg in [
        ("hero.svg", build_hero()),
        ("divider.svg", build_divider()),
        ("engines.svg", build_engines()),
    ]:
        path = os.path.join(ASSETS, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"{name:14} {os.path.getsize(path):>7,} bytes")


if __name__ == "__main__":
    main()
