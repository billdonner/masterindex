#!/usr/bin/env python3
"""Rebuild pickles/manifest.json from the files in pickles/files/.

Newest file first. Titles default to the filename; override a title or add a
note by editing pickles/titles.json ({"filename": {"title": ..., "note": ...}}).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ROOT / "pickles" / "files"
TITLES = ROOT / "pickles" / "titles.json"
MANIFEST = ROOT / "pickles" / "manifest.json"

KINDS = {
    ".pdf": "pdf",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image",
    ".webp": "image", ".svg": "image",
    ".mp4": "video", ".webm": "video", ".mov": "video",
    ".md": "markdown", ".markdown": "markdown",
    ".txt": "text",
    ".html": "html", ".htm": "html",
}


def added_at(path: Path) -> str:
    """First commit date of the file, else its mtime."""
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--follow", "--format=%cI", "--", str(path)],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip().splitlines()
    if out:
        return out[-1]
    from datetime import datetime, timezone
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")


def main() -> None:
    overrides = json.loads(TITLES.read_text()) if TITLES.exists() else {}
    docs = []
    for path in FILES.iterdir():
        if not path.is_file() or path.name.startswith("."):
            continue
        meta = overrides.get(path.name, {})
        docs.append({
            "file": f"files/{path.name}",
            "title": meta.get("title") or path.stem.replace("-", " ").replace("_", " "),
            "note": meta.get("note", ""),
            "kind": KINDS.get(path.suffix.lower(), "download"),
            "added": added_at(path),
        })
    docs.sort(key=lambda d: d["added"], reverse=True)
    MANIFEST.write_text(json.dumps({"documents": docs}, indent=2) + "\n")
    print(f"{len(docs)} document(s) -> {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
