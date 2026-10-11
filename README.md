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
| [LogiPlan](https://github.com/rangulvers/LogiPlan) ([how it works](https://rangulvers.github.io/LogiPlan/how)) | Plan a factory layout and its in-plant logistics in the browser, then simulate it. Lives in its own repo. |
| [RAGE-o-meter](https://rangulvers.github.io/rage-o-meter/) ([repo](https://github.com/rangulvers/rage-o-meter)) | A Claude Code plugin that counts how often you scold your agents per session. The only AI benchmark you can trust. |
| [NoHello for Agents](https://github.com/rangulvers/nohello-agents) | One-page guide: give your coding agent the whole request in the first message, not "hey, can you help me?" |
| [Farbpunkte](https://rangulvers.github.io/farbpunkte-spiel/) ([repo](https://github.com/rangulvers/farbpunkte-spiel)) | Fast tapping game for 2 to 4 players on one screen. When your color shows up, tap it before anyone else. In German. |
| [Claude Buddy](https://github.com/rangulvers/claude-buddy) | A tiny OLED desk display that shows what Claude Code is doing, with a mascot that reacts live. hermes-buddy is the Hermes version. |
| [Argus](https://rangulvers.github.io/argus/) ([repo](https://github.com/rangulvers/argus)) | Self-hosted scanner for your home network. Finds every device, flags risky ports and known CVEs, and tells you when something new shows up. |
| [Familien-Werkstatt](https://rangulvers.github.io/familien-werkstatt/) ([repo](https://github.com/rangulvers/familien-werkstatt)) | Small interactive pages to explore with your kids, one per topic: moon phases, rainbows, magnets, the water cycle and more. In German. |
| [Pusteblume](https://rangulvers.github.io/pusteblume/) ([repo](https://github.com/rangulvers/pusteblume)) | A painted page about dandelions. Blow into your microphone and the seeds fly away. In German. |
| [PhantomCast](https://rangulvers.github.io/phantomcast/) ([repo](https://github.com/rangulvers/phantomcast)) | Projection mapping with any projector. Map videos onto walls or windows and line up the surfaces from your phone. |
| [Claude Monitor](https://github.com/rangulvers/claude-monitor) | Live dashboard for every Claude Code session on your machine: prompts, tools, sub-agents, tokens and cost. |
| [Dalli-Klick](https://github.com/rangulvers/dalli-klick) | The TV guessing game as a desktop app for parties. A picture hides under hexagon tiles, and the earlier you guess, the more points. |
| [Agent Rodeo](https://rangulvers.github.io/agent-rodeo/) ([repo](https://github.com/rangulvers/agent-rodeo)) | Different AI coding agents get the same brief: build a 3D Lego city in the browser. Click through each attempt and compare. |
| [Wiki Graph](https://wikigraph.up.railway.app) ([repo](https://github.com/rangulvers/Wiki_Graph)) | Finds the shortest path between any two Wikipedia articles and draws the links as a graph you can explore. |

## Add a project

```bash
python3 scripts/new_project.py my-project "My Project" "One sentence summary." tag1,tag2
```

This copies `templates/project/` to `projects/my-project/` and adds a **draft** entry to `projects.json`. Edit the page, then set `"status": "live"` so it shows up on the home page. Add a `thumbnail` path (16:9 image or SVG) if you want a picture on the card.

Projects that live in their own repo (like LogiPlan, Argus or Familien-Werkstatt) get a `url` (live site) and `repo` entry in `projects.json` instead of a project page. Only a thumbnail goes in `projects/<slug>/`.

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
