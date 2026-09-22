#!/usr/bin/env python3
"""Generate the GitHub profile's dimensional SVG assets from config/profile.json."""
from pathlib import Path
import json, math

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets/generated"

def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def frame(title, w, h, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(title)}. Dimensional SVG designed for GitHub README rendering.</desc>
<defs>
<linearGradient id="bg"><stop stop-color="#02050a"/><stop offset=".55" stop-color="#071522"/><stop offset="1" stop-color="#02040a"/></linearGradient>
<linearGradient id="face" x2="0" y2="1"><stop stop-color="#fff"/><stop offset=".45" stop-color="#b7f6ff"/><stop offset="1" stop-color="#257da7"/></linearGradient>
<linearGradient id="edge"><stop stop-color="#52e7ff" stop-opacity="0"/><stop offset=".5" stop-color="#e7ffff"/><stop offset="1" stop-color="#8b7dff" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#bdfbff" stop-opacity=".9"/><stop offset=".35" stop-color="#48dfff" stop-opacity=".4"/><stop offset="1" stop-color="#15527c" stop-opacity="0"/></radialGradient>
<pattern id="scan" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 .5H8" stroke="#d6faff" stroke-opacity=".025"/></pattern>
</defs><rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/><rect width="{w}" height="{h}" rx="20" fill="url(#scan)"/>{body}</svg>"""

def stars(w,h,n=45):
    return "".join(f'<circle cx="{20+(i*83)%(w-40)}" cy="{18+(i*47)%(h-36)}" r="{1+(i%3)*.35:.1f}" fill="#d7fbff" opacity="{.16+(i%6)*.06:.2f}"/>' for i in range(n))

def depth_text(text):
    layers = "".join(f'<text x="600" y="{355+d*5}" fill="#082238" fill-opacity="{.22+d*.018:.2f}" font-family="Inter,Arial,sans-serif" font-size="60" font-weight="800" text-anchor="middle" letter-spacing="5">{esc(text)}</text>' for d in range(10,0,-1))
    return layers + f'<text x="600" y="355" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="60" font-weight="800" text-anchor="middle" letter-spacing="5">{esc(text)}</text>'

def hero():
    return frame("Krishna Sai Channalli — 3D profile identity",1200,500,
        stars(1200,500)+
        '<path d="M70 110H1130M140 400H1060" stroke="#55e7ff" stroke-opacity=".16"/>'+
        '<path d="M220 430L600 120L980 430M330 430L600 205L870 430" fill="none" stroke="#55e7ff" stroke-opacity=".08"/>'+
        '<ellipse cx="600" cy="230" rx="280" ry="105" fill="none" stroke="url(#edge)" stroke-width="1.5" stroke-dasharray="18 11"/>'+
        '<ellipse cx="600" cy="230" rx="190" ry="145" fill="none" stroke="#67eaff" stroke-opacity=".18" transform="rotate(-25 600 230)"/>'+
        '<circle cx="600" cy="230" r="135" fill="url(#glow)" opacity=".42"/><circle cx="600" cy="230" r="74" fill="none" stroke="#9df6ff" stroke-opacity=".42"/><circle cx="600" cy="230" r="48" fill="#061a29" stroke="#9df6ff" stroke-opacity=".72"/><circle cx="600" cy="230" r="13" fill="#dffeff"/>'+
        '<text x="62" y="58" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">PERSONAL ENGINEERING PROFILE</text>'+
        '<text x="1138" y="58" fill="#7896a6" font-family="monospace" font-size="10" text-anchor="end" letter-spacing="2">DEPTH / 3D TYPOGRAPHY</text>'+
        depth_text(CFG["identity"]["name"].upper())+
        '<text x="600" y="397" fill="#d9faff" font-family="Inter,Arial,sans-serif" font-size="19" text-anchor="middle" letter-spacing="4">COMPUTER SCIENCE ENGINEER</text>'+
        '<text x="600" y="431" fill="#76eaff" font-family="monospace" font-size="13" text-anchor="middle" letter-spacing="3">AI SYSTEMS · AGENTS · AUTOMATION</text>')

def technology():
    groups=list(CFG["technologies"].items())
    positions=[(170,160),(410,105),(790,105),(1030,160),(1020,390),(790,455),(410,455),(170,390)]
    colors=["#56eaff","#a78bfa","#60a5fa","#72e8c1","#6ee7b7","#f6b45f","#73d7ff","#b8c4d1"]
    body=stars(1200,540,55)+'<text x="55" y="50" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">TECHNOLOGY FIELD</text><text x="55" y="76" fill="#91afbd" font-family="monospace" font-size="10">FULL STACK / AI / AUTOMATION / INFRASTRUCTURE</text>'
    body+='<ellipse cx="600" cy="280" rx="230" ry="145" fill="none" stroke="#5ee9ff" stroke-opacity=".2" stroke-dasharray="15 10"/><ellipse cx="600" cy="280" rx="150" ry="210" fill="none" stroke="#5ee9ff" stroke-opacity=".12" transform="rotate(25 600 280)"/><circle cx="600" cy="280" r="105" fill="url(#glow)" opacity=".2"/><circle cx="600" cy="280" r="52" fill="#061a2a" stroke="#86efff"/><text x="600" y="276" fill="#eaffff" font-family="monospace" font-size="12" text-anchor="middle">ENGINEERING</text><text x="600" y="296" fill="#77eaff" font-family="monospace" font-size="9" text-anchor="middle">STACK</text>'
    for (key,items),(x,y),c in zip(groups,positions,colors):
        body+=f'<path d="M600 280Q{(600+x)//2} {(280+y)//2-35} {x} {y}" fill="none" stroke="{c}" stroke-opacity=".4" stroke-dasharray="5 11"/><circle cx="{x}" cy="{y}" r="31" fill="#071827" stroke="{c}" stroke-opacity=".85"/><text x="{x}" y="{y+4}" fill="url(#face)" font-family="Inter,Arial,sans-serif" font-size="11" font-weight="700" text-anchor="middle">{esc(key.upper())}</text>'
        for j,item in enumerate(items[:4]):
            body+=f'<text x="{x}" y="{y+54+j*15}" fill="#c8e4ed" font-family="monospace" font-size="9" text-anchor="middle">{esc(item)}</text>'
    return frame("Dimensional technology field",1200,540,body)

def project_constellation():
    body=stars(1000,430,40)+'<text x="50" y="52" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">PROJECT CONSTELLATION</text><path d="M110 335Q500 65 890 335" fill="none" stroke="url(#edge)" stroke-opacity=".5" stroke-dasharray="6 12"/><ellipse cx="500" cy="220" rx="300" ry="125" fill="none" stroke="#5ce9ff" stroke-opacity=".16"/><circle cx="500" cy="220" r="58" fill="url(#glow)" opacity=".45"/><circle cx="500" cy="220" r="36" fill="#061b2b" stroke="#8af2ff"/><text x="500" y="216" fill="#eaffff" font-family="monospace" font-size="10" text-anchor="middle">CURRENT</text><text x="500" y="232" fill="#7cefff" font-family="monospace" font-size="9" text-anchor="middle">BUILD</text>'
    positions=[(190,250),(380,130),(620,130),(810,250)]
    for (name,url,desc,stack),(x,y) in zip(CFG["projects"],positions):
        body+=f'<a href="{esc(url)}"><circle cx="{x}" cy="{y}" r="38" fill="#071a2b" stroke="#6eeaff"/><circle cx="{x}" cy="{y}" r="16" fill="#68eaff" opacity=".25"/><text x="{x}" y="{y+4}" fill="#eaffff" font-family="monospace" font-size="8" text-anchor="middle">{esc(name.upper()[:14])}</text><text x="{x}" y="{y+57}" fill="#a8cbd7" font-family="monospace" font-size="8" text-anchor="middle">{esc(desc[:31])}</text></a>'
    return frame("Project constellation",1000,430,body)

def opero():
    body=stars(1000,430,35)+'<text x="50" y="52" fill="#7feeff" font-family="monospace" font-size="12" letter-spacing="3">THE-OPERO / EXECUTION LOOP</text><ellipse cx="500" cy="220" rx="300" ry="125" fill="none" stroke="url(#edge)" stroke-width="1.5" stroke-dasharray="16 10"/><circle cx="500" cy="220" r="58" fill="url(#glow)" opacity=".4"/><circle cx="500" cy="220" r="37" fill="#061b2b" stroke="#8af2ff"/><text x="500" y="217" fill="#eaffff" font-family="monospace" font-size="11" text-anchor="middle">OPERO</text><text x="500" y="233" fill="#7cefff" font-family="monospace" font-size="8" text-anchor="middle">CORE</text>'
    steps=["SPEAK","UNDERSTAND","INVESTIGATE","DECIDE","ACT","VERIFY","REPORT"]
    for i,step in enumerate(steps):
        a=-math.pi/2+i*2*math.pi/len(steps); x=500+270*math.cos(a); y=220+105*math.sin(a)
        body+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="27" fill="#071a2b" stroke="#67eaff"/><text x="{x:.0f}" y="{y+4:.0f}" fill="#eaffff" font-family="monospace" font-size="8" text-anchor="middle">{step}</text>'
    body+='<text x="500" y="385" fill="#91b0be" font-family="monospace" font-size="9" text-anchor="middle" letter-spacing="1.5">VOICE / TOOLS / APPROVAL / EXECUTION / VERIFICATION</text>'
    return frame("The-Opero execution loop",1000,430,body)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assets={"hero-depth.svg":hero(),"technology-field.svg":technology(),"project-constellation.svg":project_constellation(),"opero-loop.svg":opero()}
    for name,data in assets.items():
        (OUT/name).write_text(data,encoding="utf-8")
    print(f"Generated {len(assets)} SVG assets.")

if __name__=="__main__":
    main()
