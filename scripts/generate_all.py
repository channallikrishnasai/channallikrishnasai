#!/usr/bin/env python3
"""Generate profile SVGs. Standard library only; optionally fetches live GitHub data."""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
PROFILE, STATS = ROOT / "assets/profile", ROOT / "assets/stats"

def esc(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def svg(title: str, width: int, height: int, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(title)} — a personal developer-profile visualization.</desc><defs><radialGradient id="atmo"><stop stop-color="#0a3156" stop-opacity=".7"/><stop offset=".55" stop-color="#07111f" stop-opacity=".45"/><stop offset="1" stop-color="#02040a"/></radialGradient><linearGradient id="line" x2="1" y2="1"><stop stop-color="#50e6ff"/><stop offset="1" stop-color="#8a6cff"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="scan" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 0h8" stroke="#9defff" stroke-opacity=".045"/></pattern></defs><rect width="100%" height="100%" rx="18" fill="url(#atmo)"/><rect width="100%" height="100%" rx="18" fill="url(#scan)"/>{body}</svg>'''

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")

def hero() -> str:
    particles = ''.join(f'<circle cx="{(i*83)%1160+20}" cy="{(i*47)%500+20}" r="{1+i%3}" fill="#8defff" opacity=".{2+i%5}"><animate attributeName="opacity" values=".15;.8;.15" dur="{4+i%5}s" repeatCount="indefinite"/></circle>' for i in range(42))
    rings = ''.join(f'<ellipse cx="600" cy="285" rx="{120+i*42}" ry="{38+i*15}" fill="none" stroke="url(#line)" stroke-opacity=".{7-i}" stroke-width="1"><animateTransform attributeName="transform" type="rotate" from="0 600 285" to="360 600 285" dur="{20+i*8}s" repeatCount="indefinite"/></ellipse>' for i in range(3))
    return svg("Krishna Sai Channalli — developer profile",1200,620,f'''{particles}<path d="M0 530H1200M100 620l250-240m100 240 150-240m100 240 0-240m100 240-150-240m500 240-250-240" stroke="#44dfff" stroke-opacity=".16"/><g filter="url(#glow)">{rings}<circle cx="600" cy="285" r="78" fill="#061b31" stroke="#66e5ff"/><circle cx="600" cy="285" r="35" fill="#9df5ff"><animate attributeName="r" values="30;39;30" dur="3s" repeatCount="indefinite"/></circle></g><g fill="#dffaff" font-family="Inter,Arial,sans-serif" text-anchor="middle"><text x="600" y="130" font-size="14" letter-spacing="6" opacity=".7">PERSONAL DEVELOPER PROFILE</text><text x="600" y="455" font-size="42" font-weight="700" letter-spacing="4">KRISHNA SAI CHANNALLI</text><text x="600" y="488" font-size="15" letter-spacing="3" fill="#75e9ff">AI SYSTEMS / AGENT ENGINEERING</text><text x="600" y="550" font-size="12" letter-spacing="2" opacity=".7">BUILDING INTELLIGENT SYSTEMS THAT SEE · SPEAK · THINK · ACT</text></g>''')

def boot() -> str:
    rows = ["AI RUNTIME", "AGENT ENGINE", "COMPUTER VISION", "VOICE INTERFACE", "AUTOMATION LAYER", "DEVELOPMENT CORE"]
    line = ''.join(f'<g opacity="0"><text x="65" y="{110+i*42}" fill="#87f4c0" font-size="17">✓</text><text x="96" y="{110+i*42}" fill="#dffaff" font-size="15">{r}</text><text x="450" y="{110+i*42}" fill="#87f4c0" font-size="13">ONLINE</text><animate attributeName="opacity" to="1" begin="{i*.35}s" dur=".25s" fill="freeze"/></g>' for i,r in enumerate(rows))
    return svg("Krishna Sai Channalli system status",640,390,f'<text x="65" y="62" fill="#75e9ff" font-family="monospace" font-size="14" letter-spacing="2">KRISHNA.SAI // SYSTEM STATUS</text><rect x="45" y="78" width="550" height="278" rx="10" fill="#020812" stroke="#1d6f9c"/>{line}<path d="M65 330h510" stroke="#2fbbd9" stroke-opacity=".45"/><text x="65" y="348" fill="#87f4c0" font-family="monospace" font-size="13">SYSTEM STATUS: OPERATIONAL</text>')

def identity() -> str:
    return svg("Digital identity for Krishna Sai Channalli",640,370,'''<g transform="translate(150 190)" fill="none" stroke="url(#line)"><circle r="105" stroke-opacity=".35"/><circle r="78" stroke-dasharray="4 10"/><path d="M-42 45c0-50 84-50 84 0M-34-25a34 34 0 1 1 68 0 34 34 0 0 1-68 0" stroke-width="3"/><ellipse rx="135" ry="42" transform="rotate(-20)" opacity=".6"><animateTransform attributeName="transform" type="rotate" from="-20 0 0" to="340 0 0" dur="18s" repeatCount="indefinite"/></ellipse></g><g font-family="Inter,Arial,sans-serif"><text x="305" y="112" fill="#75e9ff" font-size="13" letter-spacing="3">DIGITAL IDENTITY</text><text x="305" y="166" fill="#effcff" font-size="26" font-weight="700">KRISHNA SAI</text><text x="305" y="197" fill="#effcff" font-size="26" font-weight="700">CHANNALLI</text><text x="305" y="236" fill="#b9d9e8" font-size="15">Computer Science Engineer</text><text x="305" y="268" fill="#75e9ff" font-size="14">AI · AGENTS · VISION · AUTOMATION</text><text x="305" y="314" fill="#88a9ba" font-size="12">ABSTRACT IDENTITY SIGNAL — NO PORTRAIT SOURCE PROVIDED</text></g>''')

def network() -> str:
    nodes=[("PYTHON",320,190),("AI AGENTS",475,100),("COMPUTER\nVISION",560,235),("VOICE AI",420,305),("AUTOMATION",225,305)]
    links=''.join(f'<path d="M320 190L{x} {y}" stroke="#4ae3ff" stroke-opacity=".35"/>' for _,x,y in nodes[1:])
    items=''.join(f'<g><circle cx="{x}" cy="{y}" r="42" fill="#06182a" stroke="url(#line)"/><text x="{x}" y="{y-4 if "\\n" in n else y+5}" fill="#e5fbff" font-family="monospace" font-size="11" text-anchor="middle">{n.replace("\\n","</text><text x=\"%s\" y=\"%s\">"%(x,y+11))}</text></g>' for n,x,y in nodes)
    return svg("Technology focus network",640,390,f'<text x="42" y="48" fill="#75e9ff" font-family="monospace" font-size="13" letter-spacing="3">TECHNOLOGY NETWORK // VERIFIED FOCUS</text>{links}{items}<text x="42" y="360" fill="#88a9ba" font-family="monospace" font-size="11">Configured from profile.json. Add only technologies supported by public work.</text>')

def missions() -> str:
    projects=CFG.get("projects",[])
    if not projects: return svg("Mission Control",900,250,'<text x="55" y="65" fill="#75e9ff" font-family="monospace" font-size="14" letter-spacing="3">MISSION CONTROL</text><rect x="45" y="90" width="810" height="110" rx="12" fill="#05101d" stroke="#23698e"/><text x="70" y="140" fill="#e5fbff" font-family="Inter,Arial" font-size="18">MISSION QUEUE AWAITING VERIFIED PROJECT DATA</text><text x="70" y="172" fill="#88a9ba" font-family="monospace" font-size="12">Add public repositories to config/profile.json, then regenerate.</text>')
    cards=''.join(f'<g transform="translate({40+i*285} 70)"><rect width="250" height="190" rx="12" fill="#05101d" stroke="#23698e"/><text x="22" y="35" fill="#75e9ff" font-family="monospace" font-size="11">MISSION {i+1:02}</text><text x="22" y="73" fill="#effcff" font-family="Inter,Arial" font-size="20">{esc(p["name"])}</text><text x="22" y="108" fill="#b9d9e8" font-family="Inter,Arial" font-size="12">{esc(p["description"])}</text><text x="22" y="158" fill="#87f4c0" font-family="monospace" font-size="11">STATUS: {esc(p.get("status","ACTIVE"))}</text></g>' for i,p in enumerate(projects[:3]))
    return svg("Mission Control",900,300,f'<text x="40" y="40" fill="#75e9ff" font-family="monospace" font-size="14" letter-spacing="3">MISSION CONTROL</text>{cards}')

def github_data(token: str | None) -> dict | None:
    if not token: return None
    req=urllib.request.Request(f'https://api.github.com/users/{CFG["username"]}',headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","User-Agent":"profile-svg-generator"})
    try:
        with urllib.request.urlopen(req,timeout=20) as response: data = json.load(response)
        query = {"query": "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}", "variables": {"login": CFG["username"]}}
        graph = urllib.request.Request('https://api.github.com/graphql', data=json.dumps(query).encode(), headers={"Authorization":f"Bearer {token}", "Content-Type":"application/json", "User-Agent":"profile-svg-generator"})
        with urllib.request.urlopen(graph,timeout=20) as response: data["contributions"] = json.load(response).get("data",{}).get("user",{}).get("contributionsCollection",{}).get("contributionCalendar",{}).get("weeks",[])
        return data
    except Exception as err:
        print(f'warning: live GitHub data unavailable: {err}',file=sys.stderr); return None

def activity(data: dict | None) -> str:
    if not data: return svg("GitHub activity status",640,230,'<text x="45" y="60" fill="#75e9ff" font-family="monospace" font-size="14">GITHUB ACTIVITY // LIVE DATA PENDING</text><text x="45" y="115" fill="#dffaff" font-family="Inter,Arial" font-size="18">No authenticated public-data snapshot is available.</text><text x="45" y="150" fill="#88a9ba" font-family="monospace" font-size="12">The scheduled workflow refreshes this panel with GitHub API data.</text>')
    rows=[("PUBLIC REPOSITORIES",data.get("public_repos",0)),("FOLLOWERS",data.get("followers",0)),("PUBLIC GISTS",data.get("public_gists",0))]
    body=''.join(f'<text x="60" y="{110+i*35}" fill="#b9d9e8" font-family="monospace" font-size="13">{k}</text><text x="510" y="{110+i*35}" fill="#87f4c0" font-family="monospace" font-size="15">{v}</text>' for i,(k,v) in enumerate(rows))
    return svg("Live GitHub public account activity",640,250,f'<text x="60" y="58" fill="#75e9ff" font-family="monospace" font-size="14">GITHUB ACTIVITY // PUBLIC API SNAPSHOT</text>{body}<text x="60" y="218" fill="#88a9ba" font-family="monospace" font-size="11">REFRESHED {datetime.now(timezone.utc).strftime("%Y-%m-%d UTC")}</text>')

def matrix(data: dict | None) -> str:
    weeks = (data or {}).get("contributions", [])
    if not weeks:
        return svg("Contribution matrix awaiting verified GitHub data",640,180,'<text x="45" y="40" fill="#75e9ff" font-family="monospace" font-size="13">CONTRIBUTION MATRIX // DATA-SAFE MODE</text><text x="45" y="92" fill="#dffaff" font-family="Inter,Arial" font-size="16">No contribution data has been fetched.</text><text x="45" y="125" fill="#88a9ba" font-family="monospace" font-size="11">The scheduled workflow uses GitHub GraphQL to render actual contribution counts.</text>')
    max_count = max((d.get("contributionCount",0) for w in weeks for d in w.get("contributionDays",[])), default=1) or 1
    cells=[]
    for x,week in enumerate(weeks[-48:]):
        for y,day in enumerate(week.get("contributionDays",[])):
            count=day.get("contributionCount",0); opacity=.12+.88*(count/max_count)
            cells.append(f'<rect x="{44+x*11}" y="{62+y*15}" width="7" height="10" rx="2" fill="#50e6ff" opacity="{opacity:.2f}"><title>{esc(day.get("date"))}: {count} contributions</title></rect>')
    return svg("Real GitHub contribution matrix",640,210,f'<text x="45" y="40" fill="#75e9ff" font-family="monospace" font-size="13">CONTRIBUTION MATRIX // LAST 48 WEEKS</text>{"".join(cells)}<text x="45" y="188" fill="#88a9ba" font-family="monospace" font-size="11">COLOR INTENSITY REPRESENTS ACTUAL DAILY CONTRIBUTION COUNT.</text>')

def connect() -> str:
    gh,li=CFG['links']['github'],CFG['links']['linkedin']
    return svg("Connection portal",640,250,f'<text x="50" y="55" fill="#75e9ff" font-family="monospace" font-size="14" letter-spacing="3">ESTABLISH CONNECTION</text><rect x="50" y="85" width="250" height="100" rx="12" fill="#06182a" stroke="#2ba5cc"/><rect x="340" y="85" width="250" height="100" rx="12" fill="#06182a" stroke="#7967d9"/><a href="{esc(gh)}"><text x="80" y="125" fill="#effcff" font-family="Inter,Arial" font-size="18">GITHUB ↗</text><text x="80" y="153" fill="#88a9ba" font-family="monospace" font-size="10">@channallikrishnasai</text></a><a href="{esc(li)}"><text x="370" y="125" fill="#effcff" font-family="Inter,Arial" font-size="18">LINKEDIN ↗</text><text x="370" y="153" fill="#88a9ba" font-family="monospace" font-size="10">KRISHNA SAI CHANNALLI</text></a>')

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--token',default=os.getenv('GITHUB_TOKEN')); args=parser.parse_args()
    for path,content in [(PROFILE/'hero.svg',hero()),(PROFILE/'system-boot.svg',boot()),(PROFILE/'identity.svg',identity()),(PROFILE/'network.svg',network()),(PROFILE/'missions.svg',missions()),(PROFILE/'connect.svg',connect())]: write(path,content)
    data=github_data(args.token)
    write(STATS/'activity.svg',activity(data)); write(STATS/'contribution-matrix.svg',matrix(data))
    print('Generated 8 SVG assets.')
if __name__ == '__main__': main()
