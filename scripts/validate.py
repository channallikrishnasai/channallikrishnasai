#!/usr/bin/env python3
"""Validate generated SVGs, README asset references, and workflow presence."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for path in (ROOT/'assets').rglob('*.svg'):
    try: ET.parse(path)
    except ET.ParseError as exc: errors.append(f'{path}: {exc}')
readme=(ROOT/'README.md').read_text(encoding='utf-8')
for ref in re.findall(r'(?:\(|src=")(assets/[^\)"]+\.(?:svg|png|gif))',readme):
    if not (ROOT/ref).is_file(): errors.append(f'Missing README asset: {ref}')
    elif (ROOT/ref).stat().st_size == 0: errors.append(f'Empty README asset: {ref}')
for path, limit in ((ROOT/'assets/generated/nexus-hero.gif', 5_000_000), (ROOT/'assets/projects/opero-core.png', 4_000_000), (ROOT/'assets/terminal/nexus-terminal.gif', 2_000_000)):
    if path.is_file() and path.stat().st_size > limit: errors.append(f'Asset exceeds budget: {path.relative_to(ROOT)}')
if not (ROOT/'.github/workflows/update-profile.yml').is_file(): errors.append('Missing update workflow')
expected = {"hero.svg", "boot-sequence.svg", "identity.svg", "neural-constellation.svg", "mission-control.svg", "opero-core.svg", "terminal.svg", "engineering-philosophy.svg", "github-activity.svg", "contribution-matrix.svg", "connection.svg"}
actual = {path.name for path in (ROOT / "assets/nexus").glob("*.svg")} if (ROOT / "assets/nexus").is_dir() else set()
if expected - actual: errors.append(f'Missing NEXUS assets: {", ".join(sorted(expected - actual))}')
public_text = readme + "\n" + "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "assets/nexus").glob("*.svg"))
forbidden = ("awaiting", "placeholder", "todo", "withheld", "data unavailable")
for word in forbidden:
    if word in public_text.lower(): errors.append(f'Forbidden public placeholder text: {word}')
config = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
for project in config.get("projects", []):
    if not project.get("url", "").startswith("https://github.com/channallikrishnasai/"):
        errors.append(f'Invalid project URL: {project.get("url", "")})')
for candidate in ROOT.rglob('*'):
    if candidate.is_file() and '.git' not in candidate.parts and 'scripts' not in candidate.relative_to(ROOT).parts and candidate.suffix not in {'.svg', '.pyc'}:
        if re.search(r'(ghp_|github_pat_|sk-[A-Za-z0-9]{16,})', candidate.read_text(encoding='utf-8', errors='ignore')):
            errors.append(f'Potential secret in {candidate.relative_to(ROOT)}')
if errors: print('\n'.join(errors)); sys.exit(1)
print('Validation passed: SVG XML and README references are valid.')
