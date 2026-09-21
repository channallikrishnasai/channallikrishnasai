#!/usr/bin/env python3
"""Validate generated SVGs, README asset references, and workflow presence."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for path in (ROOT/'assets').rglob('*.svg'):
    try: ET.parse(path)
    except ET.ParseError as exc: errors.append(f'{path}: {exc}')
readme=(ROOT/'README.md').read_text(encoding='utf-8')
for ref in re.findall(r'\((assets/[^)]+\.svg)\)',readme):
    if not (ROOT/ref).is_file(): errors.append(f'Missing README asset: {ref}')
if not (ROOT/'.github/workflows/update-profile.yml').is_file(): errors.append('Missing update workflow')
if errors: print('\n'.join(errors)); sys.exit(1)
print('Validation passed: SVG XML and README references are valid.')
