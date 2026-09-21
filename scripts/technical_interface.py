"""Small, reusable depth-focused SVG accents for the Markdown-first profile."""
from __future__ import annotations

from datetime import datetime, timezone
from html import escape

W = 1200


def _svg(title: str, height: int, body: str) -> str:
    title = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{title}. The graphic has a readable static state when animation is unavailable.</desc>
<defs>
  <linearGradient id="face" x2="0" y2="1"><stop stop-color="#f5fdff"/><stop offset=".38" stop-color="#8cefff"/><stop offset="1" stop-color="#227da8"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop stop-color="#7cefff" stop-opacity="0"/><stop offset=".5" stop-color="#e7ffff" stop-opacity=".85"/><stop offset="1" stop-color="#7cefff" stop-opacity="0"/></linearGradient>
  <pattern id="grain" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 .5H8" stroke="#bdefff" stroke-opacity=".025"/></pattern>
</defs>
<rect width="1200" height="{height}" rx="18" fill="#03070d"/><rect width="1200" height="{height}" rx="18" fill="url(#grain)"/>{body}</svg>'''


def _label(x: int, y: int, value: str, scale: float, opacity: float, delay: float) -> str:
    safe, size = escape(value.upper()), int(17 * scale)
    depth = ''.join(f'<text x="{x + offset}" y="{y + offset}" fill="#082237" fill-opacity="{opacity * (0.28 - offset * .025):.2f}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="700" letter-spacing="1.2">{safe}</text>' for offset in range(8, 1, -1))
    return f'''<g opacity="{opacity}"><animateTransform attributeName="transform" type="translate" values="{int((x-600)*.06)} {int((y-250)*.06)};0 0;0 0" dur="1.6s" begin="{delay}s" fill="freeze"/>{depth}
<text x="{x}" y="{y}" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="700" letter-spacing="1.2">{safe}</text></g>'''


def _kicker(number: str, label: str) -> str:
    return f'<text x="62" y="54" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">{number} // {escape(label.upper())}</text>'


def _depth_panel(x: int, y: int, width: int, height: int, title: str, sub: str, stack: str, href: str, delay: float) -> str:
    right, bottom = 16, 13
    return f'''<a href="{escape(href, quote=True)}"><g>
<animateTransform attributeName="transform" type="translate" values="{int((x-600)*.08)} {int((y-280)*.08)};0 0;0 0" dur="1.4s" begin="{delay}s" fill="freeze"/>
<path d="M{x+width} {y}l{right} {bottom}v{height}l-{right} -{bottom}z" fill="#061827" stroke="#14516f"/><path d="M{x} {y+height}h{width}l{right} {bottom}H{x+right}z" fill="#04101c" stroke="#14516f"/>
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="#071522" stroke="#4edff8" stroke-opacity=".72"/><path d="M{x+14} {y+17}H{x+width-14}" stroke="#ddffff" stroke-opacity=".55"/>
<text x="{x+22}" y="{y+54}" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" letter-spacing="2">{escape(title.upper())}</text>
<text x="{x+22}" y="{y+83}" fill="#a8c4d2" font-family="monospace" font-size="11">{escape(sub.upper())}</text><text x="{x+22}" y="{y+113}" fill="#78eaff" font-family="monospace" font-size="10">{escape(stack.upper())}</text>
<path d="M{x+22} {y+136}H{x+width-22}" stroke="#4de2fa" stroke-opacity=".24" stroke-dasharray="9 12"><animate attributeName="stroke-dashoffset" values="0;-63" dur="{6 + delay}s" repeatCount="indefinite"/></path></g></a>'''


def hero(cfg: dict) -> str:
    name = escape(cfg['identity']['name'].upper())
    shadows = ''.join(f'<text x="600" y="{253 + i * 7}" fill="#0b2840" fill-opacity="{.50 - i * .045:.2f}" font-family="Inter,Arial,sans-serif" font-size="68" font-weight="800" text-anchor="middle" letter-spacing="7">{name}</text>' for i in range(8, 0, -1))
    body = f'''{_kicker('00', 'NEXUS / PERSONAL ENGINEERING INTERFACE')}<text x="1138" y="54" fill="#7896a6" font-family="monospace" font-size="10" text-anchor="end" letter-spacing="2">FRONT FACE / DEPTH 08</text><path d="M96 104H1104" stroke="#56dff7" stroke-opacity=".18"/>
<g><animateTransform attributeName="transform" type="translate" values="0 -11;0 0;0 0" dur="1.5s" fill="freeze"/><text x="600" y="128" fill="#86edff" font-family="monospace" font-size="15" text-anchor="middle" letter-spacing="9">N E X U S</text>{shadows}
<text x="600" y="253" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="68" font-weight="800" text-anchor="middle" letter-spacing="7">{name}</text><text x="600" y="305" fill="#d9faff" font-family="Inter,Arial,sans-serif" font-size="20" text-anchor="middle" letter-spacing="4">COMPUTER SCIENCE ENGINEER</text><text x="600" y="350" fill="#76eaff" font-family="monospace" font-size="14" text-anchor="middle" letter-spacing="3">AI SYSTEMS · AGENTS · AUTOMATION</text></g>
<path d="M190 385H1010" stroke="#60e7fb" stroke-opacity=".48" stroke-dasharray="70 750"><animate attributeName="stroke-dashoffset" values="-820;820" dur="7.5s" repeatCount="indefinite"/></path><text x="600" y="423" fill="#9bb8c5" font-family="monospace" font-size="11" text-anchor="middle" letter-spacing="1.5">BUILDING INTELLIGENT SYSTEMS THAT SEE · SPEAK · THINK · ACT</text>'''
    return _svg('NEXUS depth typography — Krishna Sai Channalli', 460, body)


def technology_wall() -> str:
    labels = [(112,145,'Python',1.35,1,.1),(365,112,'TypeScript',1.08,.78,.3),(790,150,'React',1.22,.92,.2),(1000,112,'Rust',.92,.55,.45),(190,280,'FastAPI',1.08,.88,.42),(485,252,'Next.js',1.1,1,.25),(780,290,'PostgreSQL',1.06,.8,.55),(1015,270,'Docker',.92,.6,.6),(300,397,'Gemini',.88,.55,.7),(548,375,'Prisma',.92,.68,.63),(745,420,'PyQt6',.92,.62,.8),(960,395,'OpenTelemetry',.72,.36,.75)]
    body = _kicker('01', 'Technology wall') + '<text x="62" y="80" fill="#91afbd" font-family="monospace" font-size="10" letter-spacing="1.5">VISUAL DEPTH IS COMPOSITIONAL — NOT A PROFICIENCY RANKING.</text><path d="M75 458L1125 458" stroke="#58e5fa" stroke-opacity=".2"/><path d="M135 130L1065 432M185 100L1115 402" stroke="#59e4fa" stroke-opacity=".08"/>' + ''.join(_label(*label) for label in labels)
    return _svg('Dimensional technology wall with verified technologies', 500, body)


def project_composition(cfg: dict) -> str:
    p = cfg['projects']
    panels = [(110,112,535,155,p[0]['name'],'Local desktop AI operator','Python · PyQt6 · Gemini',p[0]['repository'],.1),(690,168,390,148,p[1]['name'],'Personal-finance intelligence','Next.js · TypeScript · Prisma',p[1]['repository'],.38),(295,348,410,148,p[2]['name'],'AI life management','FastAPI · React · PostgreSQL',p[2]['repository'],.55),(760,374,330,140,p[3]['name'].split(' / ')[0],'Code intelligence','Go · tree-sitter · local index',p[3]['repository'],.72)]
    body = _kicker('03', 'Selected systems') + '<text x="62" y="80" fill="#91afbd" font-family="monospace" font-size="10" letter-spacing="1.5">DEPTH POSITIONS ARE EDITORIAL; PROJECT DETAILS AND LINKS FOLLOW IN MARKDOWN.</text><path d="M65 534H1135" stroke="#5de9fa" stroke-opacity=".16"/>' + ''.join(_depth_panel(*panel) for panel in panels)
    return _svg('Dimensional composition of selected public projects', 570, body)


def pipeline(title: str, kicker: str, stages: list[str], subtitle: str) -> str:
    start, gap, y = 46, 163, 183
    blocks = []
    for index, stage in enumerate(stages):
        x = start + index * gap
        blocks.append(f'''<g><animateTransform attributeName="transform" type="translate" values="0 {16 if index % 2 else -16};0 0;0 0" dur="1.25s" begin="{index*.14}s" fill="freeze"/><path d="M{x+130} {y-27}l10 9v55l-10 -9z" fill="#082033"/><path d="M{x} {y+28}h130l10 9H{x+10}z" fill="#05111e"/><rect x="{x}" y="{y-27}" width="130" height="55" rx="5" fill="#081827" stroke="#65eafb" stroke-opacity=".7"/><text x="{x+65}" y="{y+5}" fill="#e7ffff" font-family="monospace" font-size="9" text-anchor="middle">{escape(stage)}</text></g>''')
    line = f'<path d="M{start} {y}H{start+(len(stages)-1)*gap+130}" stroke="#88f3ff" stroke-width="2" stroke-dasharray="14 22"><animate attributeName="stroke-dashoffset" values="0;-108" dur="7s" repeatCount="indefinite"/></path>'
    return _svg(title, 275, _kicker(kicker,title) + f'<text x="62" y="80" fill="#91afbd" font-family="monospace" font-size="10" letter-spacing="1">{escape(subtitle.upper())}</text>{line}' + ''.join(blocks))


def terminal(cfg: dict) -> str:
    rows = [('profile',cfg['identity']['name']),('focus','AI / Agents / Automation'),('current',cfg['current_build']['name']),('stack','Python / TypeScript / Rust'),('status','Ready')]
    lines = ''.join(f'<text x="145" y="{140+i*38}" fill="#78eaff" font-family="monospace" font-size="13">{escape(key).ljust(10)} </text><text x="300" y="{140+i*38}" fill="#e3fbff" font-family="monospace" font-size="13">{escape(value)}</text>' for i,(key,value) in enumerate(rows))
    body = f'''{_kicker('07','Terminal')}<path d="M110 95H1064l26 18v220H136l-26-18z" fill="#04111d" stroke="#14506d"/><path d="M110 95H1064v220H110z" fill="#06131f" stroke="#61e6f8" stroke-opacity=".72"/><path d="M128 116H1046" stroke="#ddffff" stroke-opacity=".36"/><text x="145" y="126" fill="#9befff" font-family="monospace" font-size="11">nexus@krishna:~$ system</text>{lines}<text x="145" y="310" fill="#8defff" font-family="monospace" font-size="13">nexus@krishna:~$</text><rect x="300" y="297" width="9" height="16" fill="#b9ffff"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>'''
    return _svg('NEXUS profile terminal', 370, body)


def github_signal(data: dict | None) -> str:
    values = [('PUBLIC REPOSITORIES',str(data.get('public_repos',0))),('FOLLOWERS',str(data.get('followers',0))),('PUBLIC GISTS',str(data.get('public_gists',0)))] if data else []
    refreshed = 'REFRESHED ' + datetime.now(timezone.utc).strftime('%Y-%m-%d UTC') if data else 'PUBLIC METRICS REFRESH THROUGH THE SCHEDULED WORKFLOW'
    metrics = ''.join(f'<g><text x="{250+i*350}" y="150" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="700" text-anchor="middle">{escape(value)}</text><text x="{250+i*350}" y="182" fill="#9bb8c5" font-family="monospace" font-size="10" text-anchor="middle" letter-spacing="1">{label}</text><path d="M{160+i*350} 205H{340+i*350}" stroke="#69eafb" stroke-opacity=".5" stroke-dasharray="12 18"><animate attributeName="stroke-dashoffset" values="0;-60" dur="{5+i}s" repeatCount="indefinite"/></path></g>' for i,(label,value) in enumerate(values))
    return _svg('Verified public GitHub signal', 290, _kicker('06','GitHub signal') + metrics + f'<text x="600" y="256" fill="#93b0bd" font-family="monospace" font-size="10" text-anchor="middle" letter-spacing="1">{refreshed}</text>')


def render_assets(cfg: dict, data: dict | None) -> dict[str,str]:
    return {'hero-depth.svg':hero(cfg),'technology-wall.svg':technology_wall(),'project-depth.svg':project_composition(cfg),'opero-flow.svg':pipeline('The-Opero execution layers','04',['INPUT','UNDERSTAND','INVESTIGATE','DECIDE','ACT','VERIFY','REPORT'],'Repository-documented execution and response sequence'),'automation-flow.svg':pipeline('Automation layers','05',['TRIGGER','UNDERSTAND','DECIDE','EXECUTE','VERIFY','RESULT'],'A visual model of repository-supported automation work'),'github-signal.svg':github_signal(data),'terminal-depth.svg':terminal(cfg)}
