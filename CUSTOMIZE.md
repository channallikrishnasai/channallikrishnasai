# Customizing Krishna Sai // NEXUS

All editorial content lives in `config/profile.json`. It is organized into identity, domains, technologies, projects, current build, links, and visual configuration. Update only verified information there, then run:

```bash
python scripts/generate_all.py
python scripts/validate.py
```

`projects` contains public projects selected for the interface. A project entry has this shape:

```json
{
  "name": "Project name",
  "repository": "https://github.com/channallikrishnasai/project-name",
  "description": "A concise, verified description.",
  "evidence": "Technologies and capabilities evidenced by the public repository."
}
```

The included GitHub Actions workflow regenerates the two typographic depth accents weekly and on demand. No token, key, or credential is stored in the repository.

The generator writes only the hero and technology-wall effects to `assets/nexus/`; the profile's project evidence, tables, terminal, and links live as readable Markdown. Repository-native visual evidence is kept under `assets/source/`.

The SVGs use only GitHub-friendly SVG/Markdown primitives. Animation is decorative; all important text remains present in the README as alt text or regular Markdown.
