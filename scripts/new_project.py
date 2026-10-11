#!/usr/bin/env python3
"""Create a new project folder from templates/project and register it in projects.json.

Usage: python3 scripts/new_project.py my-project "My Project" "One sentence summary." tag1,tag2
"""
import json, re, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    slug, title = argv[1], argv[2]
    summary = argv[3] if len(argv) > 3 else "A new project."
    tags = [t.strip() for t in argv[4].split(",")] if len(argv) > 4 else []
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("slug must be lowercase letters, digits and hyphens, e.g. my-project")
    dest = ROOT / "projects" / slug
    if dest.exists():
        sys.exit("projects/%s already exists" % slug)
    shutil.copytree(ROOT / "templates" / "project", dest)
    for f in dest.rglob("*"):
        if f.is_file():
            f.write_text(f.read_text().replace("{{TITLE}}", title).replace("{{SUMMARY}}", summary))
    reg = ROOT / "projects.json"
    items = json.loads(reg.read_text())
    items.append({"slug": slug, "title": title, "summary": summary, "tags": tags, "status": "draft", "date": date.today().isoformat()})
    reg.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
    print("Created projects/%s and added it to projects.json as a draft." % slug)
    print('Set "status": "live" in projects.json when it should appear on the home page.')

main(sys.argv)
