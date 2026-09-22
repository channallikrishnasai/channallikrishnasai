#!/usr/bin/env python3
"""Validate the profile package."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for p in (ROOT/"assets").rglob("*.svg"):
    try: ET.parse(p)
    except ET.ParseError as e: errors.append(f"{p}: {e}")
readme=(ROOT/"README.md").read_text(encoding="utf-8")
for ref in re.findall(r'(?:\(|src=")(assets/[^\)"]+\.(?:svg|jpg|png))',readme):
    if not (ROOT/ref).is_file(): errors.append(f"Missing README asset: {ref}")
cfg=json.loads((ROOT/"config/profile.json").read_text(encoding="utf-8"))
for project in cfg["projects"]:
    if not project[1].startswith("https://github.com/channallikrishnasai/"):
        errors.append(f"Invalid project URL: {project[1]}")
for word in ("placeholder","todo","nexus","awaiting"):
    if word in (readme + (ROOT/"CUSTOMIZE.md").read_text(encoding="utf-8")).lower():
        errors.append(f"Forbidden profile branding/placeholder word: {word}")
if not (ROOT/"assets/profile/krishna-sai.jpg").is_file(): errors.append("Missing primary portrait")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("Validation passed.")
