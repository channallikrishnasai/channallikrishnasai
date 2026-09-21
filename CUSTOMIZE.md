# Customizing your profile homepage

All editorial content lives in `config/profile.json`. Update the name, focus, links, and only verified projects there, then run:

```bash
python scripts/generate_all.py
python scripts/validate.py
```

`projects` intentionally starts empty because the source profile repository was unavailable at build time. A project entry has this shape:

```json
{
  "name": "Project name",
  "description": "A concise, verified description.",
  "status": "ACTIVE",
  "url": "https://github.com/channallikrishnasai/project-name"
}
```

The included GitHub Actions workflow refreshes assets weekly and on demand. It uses the ephemeral `GITHUB_TOKEN`; no token, key, or credential is stored in the repository. The activity panel only displays API results it actually receives. The contribution panel remains explicitly data-safe until a real GraphQL contribution fetcher is configured.

The SVGs use only GitHub-friendly SVG/Markdown primitives. Animation is decorative; all important text remains present in the README as alt text or regular Markdown.
