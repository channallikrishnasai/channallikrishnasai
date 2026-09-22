#!/usr/bin/env python3
"""Generate animated 3D SVG assets for the GitHub profile from config/profile.json.

Emits SMIL animations (works in GitHub README <img> rendering):
- hero-3d.svg        animated dimensional identity
- automation-3d.svg  animated automation pipeline
"""
from pathlib import Path
import json, math

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets/generated"


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def frame(title, w, h, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(title)}. Animated 3D SVG for GitHub README.</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#01040a"/><stop offset=".45" stop-color="#061624"/><stop offset="1" stop-color="#02040c"/></linearGradient>
<linearGradient id="face" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset=".4" stop-color="#c8f9ff"/><stop offset="1" stop-color="#1f7ea8"/></linearGradient>
<linearGradient id="edge"><stop stop-color="#3ce7ff" stop-opacity="0"/><stop offset=".5" stop-color="#f0ffff"/><stop offset="1" stop-color="#9b8cff" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#c9fdff" stop-opacity=".95"/><stop offset=".35" stop-color="#3ad9ff" stop-opacity=".45"/><stop offset="1" stop-color="#0d4a70" stop-opacity="0"/></radialGradient>
<linearGradient id="flow" x1="0" x2="1"><stop stop-color="#38e8ff"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#34d399"/></linearGradient>
<pattern id="scan" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 .5H6" stroke="#d6faff" stroke-opacity=".03"/></pattern>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#scan)"/>
{body}
</svg>"""


def twinkling_stars(w, h, n=40):
    parts = []
    for i in range(n):
        x = 16 + (i * 97) % (w - 32)
        y = 14 + (i * 53) % (h - 28)
        r = 0.8 + (i % 3) * 0.4
        dur = 1.6 + (i % 5) * 0.45
        begin = (i % 7) * 0.35
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#d9fbff" opacity=".2">'
            f'<animate attributeName="opacity" values=".1;.75;.1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return "".join(parts)


def depth_text(text, cx, cy, size=58, layers=8):
    """Layered pseudo-3D text with a subtle depth breathe animation."""
    out = []
    for d in range(layers, 0, -1):
        op = 0.18 + d * 0.02
        out.append(
            f'<text x="{cx}" y="{cy + d * 4}" fill="#062033" fill-opacity="{op:.2f}" '
            f'font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="800" '
            f'text-anchor="middle" letter-spacing="4">{esc(text)}</text>'
        )
    out.append(
        f'<text x="{cx}" y="{cy}" fill="url(#face)" font-family="Segoe UI,Arial,sans-serif" '
        f'font-size="{size}" font-weight="800" text-anchor="middle" letter-spacing="4">{esc(text)}'
        f'<animate attributeName="opacity" values="1;.86;1" dur="3.2s" repeatCount="indefinite"/></text>'
    )
    return "".join(out)


def hero():
    name = CFG["identity"]["name"].upper()
    role = CFG["identity"]["role"].upper()
    tags = "AI SYSTEMS · AGENTS · AUTOMATION · FULL-STACK"
    w, h = 1200, 520
    body = []
    body.append(twinkling_stars(w, h, 48))

    # Perspective floor grid with scrolling motion (fake 3D depth)
    body.append(
        '<g opacity=".35">'
        '<path d="M0 470 L600 340 L1200 470" fill="none" stroke="#2fd4ff" stroke-opacity=".25"/>'
        '<path d="M0 490 L600 355 L1200 490" fill="none" stroke="#2fd4ff" stroke-opacity=".2"/>'
        "</g>"
    )
    for i in range(9):
        y0 = 360 + i * 16
        op = 0.06 + i * 0.02
        body.append(
            f'<path d="M{40 + i * 10} {y0} L600 {340 + i * 6} L{1160 - i * 10} {y0}" '
            f'fill="none" stroke="#5ee9ff" stroke-opacity="{op:.2f}" stroke-width="1">'
            f'<animate attributeName="stroke-opacity" values="{op:.2f};{op + 0.08:.2f};{op:.2f}" '
            f'dur="{2.4 + i * 0.2}s" repeatCount="indefinite"/></path>'
        )

    # Rotating orbital rings (3D tilt via animateTransform)
    body.append(
        '<g transform="translate(600 210)">'
        '<ellipse rx="300" ry="110" fill="none" stroke="url(#edge)" stroke-width="1.6" stroke-dasharray="22 14">'
        '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="28s" repeatCount="indefinite"/></ellipse>'
        '<ellipse rx="210" ry="150" fill="none" stroke="#67eaff" stroke-opacity=".28" transform="rotate(-22)">'
        '<animateTransform attributeName="transform" type="rotate" from="-22" to="338" dur="18s" repeatCount="indefinite"/></ellipse>'
        '<ellipse rx="140" ry="90" fill="none" stroke="#9b8cff" stroke-opacity=".35" stroke-dasharray="8 10" transform="rotate(35)">'
        '<animateTransform attributeName="transform" type="rotate" from="35" to="-325" dur="12s" repeatCount="indefinite"/></ellipse>'
        '<circle r="130" fill="url(#glow)" opacity=".4">'
        '<animate attributeName="opacity" values=".3;.55;.3" dur="4s" repeatCount="indefinite"/></circle>'
        # Core
        '<circle r="54" fill="#041622" stroke="#8af2ff" stroke-width="1.5"/>'
        '<circle r="34" fill="none" stroke="#6eeaff" stroke-opacity=".5" stroke-dasharray="4 6">'
        '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/></circle>'
        '<circle r="12" fill="#e8feff" filter="url(#soft)">'
        '<animate attributeName="r" values="10;14;10" dur="2.2s" repeatCount="indefinite"/></circle>'
        "</g>"
    )

    # Orbiting particles
    for i, (rx, ry, dur, c) in enumerate(
        [(300, 110, 10, "#5ee9ff"), (210, 150, 14, "#a78bfa"), (140, 90, 8, "#34d399")]
    ):
        body.append(
            f'<g transform="translate(600 210)">'
            f'<circle r="5" fill="{c}" filter="url(#soft)">'
            f'<animateMotion path="M {-rx} 0 A {rx} {ry} 0 1 1 {rx} 0 A {rx} {ry} 0 1 1 {-rx} 0" dur="{dur}s" repeatCount="indefinite"/>'
            f"</circle></g>"
        )

    # Corner labels
    body.append(
        '<text x="52" y="52" fill="#7feeff" font-family="ui-monospace,monospace" font-size="12" letter-spacing="3">'
        "PERSONAL ENGINEERING PROFILE"
        '<animate attributeName="opacity" values=".7;1;.7" dur="3s" repeatCount="indefinite"/></text>'
    )
    body.append(
        '<text x="1148" y="52" fill="#7896a6" font-family="ui-monospace,monospace" font-size="10" '
        'text-anchor="end" letter-spacing="2">ANIMATED / 3D / LIVE</text>'
    )

    # Name + role
    body.append(depth_text(name, 600, 372, size=56))
    body.append(
        f'<text x="600" y="418" fill="#d9faff" font-family="Segoe UI,Arial,sans-serif" font-size="18" '
        f'text-anchor="middle" letter-spacing="5">{esc(role)}</text>'
    )
    body.append(
        f'<text x="600" y="452" fill="#6ee7ff" font-family="ui-monospace,monospace" font-size="13" '
        f'text-anchor="middle" letter-spacing="3">{esc(tags)}</text>'
    )

    # Scanning line
    body.append(
        '<rect x="0" y="0" width="1200" height="2" fill="url(#flow)" opacity=".55">'
        '<animate attributeName="y" values="0;518;0" dur="6s" repeatCount="indefinite"/></rect>'
    )
    return frame("Krishna Sai Channalli — animated 3D identity", w, h, "".join(body))


def automation():
    w, h = 1200, 420
    steps = [
        ("TRIGGER", "#38e8ff"),
        ("UNDERSTAND", "#60a5fa"),
        ("DECIDE", "#a78bfa"),
        ("EXECUTE", "#f472b6"),
        ("VERIFY", "#fbbf24"),
        ("RESULT", "#34d399"),
    ]
    body = [twinkling_stars(w, h, 28)]
    body.append(
        '<text x="52" y="48" fill="#7feeff" font-family="ui-monospace,monospace" font-size="13" letter-spacing="4">'
        "AUTOMATION PIPELINE"
        '<animate attributeName="opacity" values=".65;1;.65" dur="2.8s" repeatCount="indefinite"/></text>'
    )
    body.append(
        '<text x="52" y="72" fill="#8aa6b5" font-family="ui-monospace,monospace" font-size="10" letter-spacing="2">'
        "TRIGGER → UNDERSTAND → DECIDE → EXECUTE → VERIFY → RESULT</text>"
    )

    # Base rail
    x0, x1, y = 90, 1110, 220
    body.append(
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#1a3a52" stroke-width="3" stroke-linecap="round"/>'
    )
    # Animated pulse along rail
    body.append(
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#flow)" stroke-width="3" '
        f'stroke-linecap="round" stroke-dasharray="40 980" opacity=".9">'
        f'<animate attributeName="stroke-dashoffset" values="1020;0" dur="3.2s" repeatCount="indefinite"/></line>'
    )

    # Travelling orb
    body.append(
        f'<circle r="9" fill="#e8feff" filter="url(#soft)">'
        f'<animateMotion path="M {x0} {y} L {x1} {y}" dur="3.2s" repeatCount="indefinite"/></circle>'
    )

    n = len(steps)
    for i, (label, color) in enumerate(steps):
        x = x0 + i * (x1 - x0) / (n - 1)
        delay = i * 0.35
        # Node
        body.append(
            f'<g transform="translate({x:.0f} {y})">'
            f'<circle r="34" fill="#061a2b" stroke="{color}" stroke-width="2"/>'
            f'<circle r="34" fill="none" stroke="{color}" stroke-opacity=".6" stroke-width="1">'
            f'<animate attributeName="r" values="34;48;34" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values=".7;0;.7" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/></circle>'
            f'<circle r="8" fill="{color}">'
            f'<animate attributeName="opacity" values=".5;1;.5" dur="1.6s" begin="{delay}s" repeatCount="indefinite"/></circle>'
            f'<text y="64" fill="#e7fbff" font-family="ui-monospace,monospace" font-size="12" '
            f'text-anchor="middle" letter-spacing="1">{label}</text>'
            f'<text y="84" fill="{color}" font-family="ui-monospace,monospace" font-size="9" '
            f'text-anchor="middle" opacity=".8">0{i + 1}</text>'
            f"</g>"
        )
        if i < n - 1:
            mx = (x + x0 + (i + 1) * (x1 - x0) / (n - 1)) / 2
            body.append(
                f'<text x="{mx:.0f}" y="{y - 28}" fill="#4a7a95" font-family="ui-monospace,monospace" '
                f'font-size="14" text-anchor="middle">→</text>'
            )

    # Floating status chips
    chips = [
        (140, 320, "PyQt6 · Browser · Voice"),
        (520, 340, "Agents · Tools · APIs"),
        (880, 320, "Verify · Report · Ship"),
    ]
    for i, (cx, cy, text) in enumerate(chips):
        body.append(
            f'<g transform="translate({cx} {cy})">'
            f'<rect x="-110" y="-16" width="220" height="32" rx="16" fill="#0a1f30" stroke="#2a5a78" stroke-opacity=".8"/>'
            f'<text y="5" fill="#9fe8ff" font-family="ui-monospace,monospace" font-size="11" text-anchor="middle">{esc(text)}</text>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{cx} {cy};{cx} {cy - 6};{cx} {cy}" dur="{3 + i}s" repeatCount="indefinite" additive="sum"/>'
            f"</g>"
        )

    # Bottom note
    body.append(
        '<text x="600" y="395" fill="#6d8fa3" font-family="ui-monospace,monospace" font-size="10" '
        'text-anchor="middle" letter-spacing="2">BUILD → EXPERIMENT → MEASURE → AUTOMATE → VERIFY → SHIP</text>'
    )
    return frame("Animated automation pipeline", w, h, "".join(body))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Remove legacy static SVGs no longer referenced
    legacy = ["technology-field.svg", "project-constellation.svg", "opero-loop.svg", "hero-depth.svg"]
    assets = {"hero-3d.svg": hero(), "automation-3d.svg": automation()}
    for name, data in assets.items():
        (OUT / name).write_text(data, encoding="utf-8")
    for name in legacy:
        p = OUT / name
        if p.exists():
            p.unlink()
    print(f"Generated {len(assets)} animated SVG assets.")


if __name__ == "__main__":
    main()
