#!/usr/bin/env python3
from pathlib import Path

base = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec")
missing = []

for p in sorted((base / "services").glob("*/index.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    if '<div class="breadcrumb">' not in t:
        missing.append(p)

print(f"missing: {len(missing)}")
for p in missing:
    print(p.relative_to(base))
