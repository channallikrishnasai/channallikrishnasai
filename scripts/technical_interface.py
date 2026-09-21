"""The two SVG effects that GitHub Markdown cannot render: typographic depth and light."""
from __future__ import annotations

from html import escape

W = 1200


def canvas(title: str, height: int, body: str) -> str:
    safe = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" role="img" aria-labelledby="title desc">
<title id="title">{safe}</title><desc id="desc">{safe}. The graphic remains readable without animation.</desc>
<defs>
  <linearGradient id="face" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset=".4" stop-color="#91efff"/><stop offset="1" stop-color="#257da7"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop stop-color="#7cefff" stop-opacity="0"/><stop offset=".5" stop-color="#f2ffff" stop-opacity=".9"/><stop offset="1" stop-color="#7cefff" stop-opacity="0"/></linearGradient>
  <pattern id="scan" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 .5H8" stroke="#d6faff" stroke-opacity=".025"/></pattern>
</defs>
<rect width="1200" height="{height}" rx="18" fill="#03070d"/><rect width="1200" height="{height}" rx="18" fill="url(#scan)"/>{body}</svg>'''


def depth_text(x: int, y: int, value: str, size: int, *, anchor: str = 'middle', layers: int = 8) -> str:
    value = escape(value)
    rear = ''.join(
        f'<text x="{x}" y="{y + depth * 7}" fill="#0a2539" fill-opacity="{.52 - depth * .045:.2f}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="800" text-anchor="{anchor}" letter-spacing="6">{value}</text>'
        for depth in range(layers, 0, -1)
    )
    return rear + f'<text x="{x}" y="{y}" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="800" text-anchor="{anchor}" letter-spacing="6">{value}</text>'


def hero(cfg: dict) -> str:
    name = cfg['identity']['name'].upper()
    body = f'''<text x="62" y="54" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">00 // NEXUS / PERSONAL ENGINEERING INTERFACE</text>
<text x="1138" y="54" fill="#7896a6" font-family="monospace" font-size="10" text-anchor="end" letter-spacing="2">FRONT FACE / DEPTH 08</text><path d="M96 104H1104" stroke="#56dff7" stroke-opacity=".18"/>
<g><animateTransform attributeName="transform" type="translate" values="0 -12;0 0;0 0" dur="1.5s" fill="freeze"/><text x="600" y="128" fill="#86edff" font-family="monospace" font-size="15" text-anchor="middle" letter-spacing="9">N E X U S</text>{depth_text(600,253,name,68)}
<text x="600" y="305" fill="#d9faff" font-family="Inter,Arial,sans-serif" font-size="20" text-anchor="middle" letter-spacing="4">COMPUTER SCIENCE ENGINEER</text><text x="600" y="350" fill="#76eaff" font-family="monospace" font-size="14" text-anchor="middle" letter-spacing="3">AI SYSTEMS · AGENTS · AUTOMATION</text></g>
<path d="M190 385H1010" stroke="#60e7fb" stroke-opacity=".48" stroke-dasharray="70 750"><animate attributeName="stroke-dashoffset" values="-820;820" dur="7.5s" repeatCount="indefinite"/></path><text x="600" y="423" fill="#9bb8c5" font-family="monospace" font-size="11" text-anchor="middle" letter-spacing="1.5">BUILDING INTELLIGENT SYSTEMS THAT SEE · SPEAK · THINK · ACT</text>'''
    return canvas('NEXUS depth typography — Krishna Sai Channalli', 460, body)


def label(x: int, y: int, value: str, scale: float, opacity: float, delay: float) -> str:
    safe, size = escape(value.upper()), int(17 * scale)
    depth = ''.join(f'<text x="{x+offset}" y="{y+offset}" fill="#09243a" fill-opacity="{opacity*(.28-offset*.025):.2f}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="700" letter-spacing="1.2">{safe}</text>' for offset in range(8, 1, -1))
    return f'<g opacity="{opacity}"><animateTransform attributeName="transform" type="translate" values="{int((x-600)*.06)} {int((y-250)*.06)};0 0;0 0" dur="1.6s" begin="{delay}s" fill="freeze"/>{depth}<text x="{x}" y="{y}" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="700" letter-spacing="1.2">{safe}</text></g>'


def technology_wall() -> str:
    labels = [(112,145,'Python',1.35,1,.1),(365,112,'TypeScript',1.08,.78,.3),(790,150,'React',1.22,.92,.2),(1000,112,'Rust',.92,.55,.45),(190,280,'FastAPI',1.08,.88,.42),(485,252,'Next.js',1.1,1,.25),(780,290,'PostgreSQL',1.06,.8,.55),(1015,270,'Docker',.92,.6,.6),(300,397,'Gemini',.88,.55,.7),(548,375,'Prisma',.92,.68,.63),(745,420,'PyQt6',.92,.62,.8),(960,395,'OpenTelemetry',.72,.36,.75)]
    body = '<text x="62" y="54" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">01 // TECHNOLOGY WALL</text><text x="62" y="80" fill="#91afbd" font-family="monospace" font-size="10" letter-spacing="1.5">VISUAL DEPTH IS COMPOSITIONAL — NOT A PROFICIENCY RANKING.</text><path d="M75 458L1125 458" stroke="#58e5fa" stroke-opacity=".2"/><path d="M135 130L1065 432M185 100L1115 402" stroke="#59e4fa" stroke-opacity=".08"/>' + ''.join(label(*item) for item in labels)
    return canvas('Dimensional technology wall with verified technologies', 500, body)


def render_assets(cfg: dict) -> dict[str, str]:
    return {'hero-depth.svg': hero(cfg), 'technology-wall.svg': technology_wall()}
