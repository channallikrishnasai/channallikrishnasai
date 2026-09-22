# Customizing the profile

All editable identity, technology, project, and link data lives in `config/profile.json`.

Run:

```bash
pip install pillow numpy
python scripts/render_3d.py
python scripts/validate.py
```

The renderer software-rasterizes true 3D scenes (numpy z-buffer + Pillow) into looping GIFs under `assets/generated/` — no SVG.

The supplied portrait files live under `assets/profile/`:
- `krishna-sai.jpg` — primary profile image
- `krishna-sai-editorial.jpg` — alternate supplied image

The profile intentionally has **no separate product/brand name**. The visual language is simply the engineering profile of Krishna Sai Channalli.

No API keys, tokens, or credentials are required.
