# AIProjects

A collection of small projects built with AI, shared as a website on GitHub Pages. Each project has its own folder, its own page, and its own source.

## Structure

```
index.html            home page, lists the projects from projects.json
projects.json         registry: one entry per project (title, summary, tags, status)
assets/               shared CSS and icons used by all pages
projects/
  <project-slug>/
    index.html        the project's web page
    README.md         what it is and how to rebuild it
    src/              source code, if any
    ...               PDFs, images, data
templates/project/    starting point for a new project
scripts/new_project.py  creates a project from the template
.github/workflows/pages.yml  deploys the site on every push to main
```

## Projects

| Project | What it is |
| --- | --- |
| [Rubik's Cube Guides](projects/rubiks-cube/) | Printable picture guides for kids: Layer-by-Layer and CFOP (German). |
| [LogiPlan](https://github.com/rangulvers/LogiPlan) ([live](https://rangulvers.github.io/LogiPlan/)) | Plan a factory layout and its in-plant logistics in the browser, then simulate it. Lives in its own repo. |

## Add a project

```bash
python3 scripts/new_project.py my-project "My Project" "One sentence summary." tag1,tag2
```

This copies `templates/project/` to `projects/my-project/` and adds a **draft** entry to `projects.json`. Edit the page, then set `"status": "live"` so it shows up on the home page. Add a `thumbnail` path (16:9 image or SVG) if you want a picture on the card.

Projects that live in their own repo (like LogiPlan) get a `url` (live site) and `repo` entry in `projects.json` instead of a project page. Only a thumbnail goes in `projects/<slug>/`.

Conventions: lowercase-hyphen folder names, commit generated output (HTML, PDF) so the site needs no build step, keep each project self-contained.

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. (Opening `index.html` directly will not load `projects.json`.)

## Publish

1. Create the GitHub repo `AIProjects` and push this folder to `main`.
2. In the repo, go to Settings, then Pages, and set the source to **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` deploys the site on each push. It will be at `https://<your-user>.github.io/AIProjects/`.

All links are relative, so the site works under that sub-path.
