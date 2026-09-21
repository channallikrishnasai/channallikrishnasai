# Customizing Krishna Sai // NEXUS

All editorial content lives in `config/profile.json`. Update the name, focus, links, and only verified projects there, then run:

```bash
python scripts/generate_all.py
python scripts/validate.py
```

`projects` contains public projects selected for the constellation. A project entry has this shape:

```json
{
  "name": "Project name",
  "description": "A concise, verified description.",
  "status": "ACTIVE",
  "url": "https://github.com/channallikrishnasai/project-name"
}
```

The included GitHub Actions workflow refreshes assets weekly and on demand. It uses the ephemeral `GITHUB_TOKEN`; no token, key, or credential is stored in the repository. Public repository and account data are fetched from GitHub's REST API; contribution history is fetched through GraphQL only when the workflow token is available.

The generator writes lightweight data and supporting visuals to `assets/nexus/`. Cinematic raster assets live in `assets/generated/`, `assets/projects/`, and `assets/terminal/`.

The SVGs use only GitHub-friendly SVG/Markdown primitives. Animation is decorative; all important text remains present in the README as alt text or regular Markdown.
