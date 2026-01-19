#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path

BASE_URL = "https://wattsatpcontractor.com"


CANONICAL_RE = re.compile(
    r"<link\b[^>]*\brel=[\"']canonical[\"'][^>]*>",
    flags=re.IGNORECASE,
)


def _extract_href(link_tag: str) -> str | None:
    m = re.search(r"\bhref=[\"']([^\"']+)[\"']", link_tag, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None


def _desired_canonical_for(file_path: Path, base_dir: Path) -> str:
    rel = file_path.relative_to(base_dir).as_posix()

    # Homepage
    if rel == "index.html":
        return f"{BASE_URL}/"

    # Services detail pages
    if rel.startswith("services/") and rel.endswith("/index.html"):
        slug = rel[len("services/") : -len("/index.html")]
        return f"{BASE_URL}/services/{slug}/"

    # Root .html pages
    if "/" not in rel and rel.endswith(".html"):
        name = rel[:-5]
        return f"{BASE_URL}/{name}"

    # Fallback: directory index
    if rel.endswith("/index.html"):
        folder = rel[:-len("/index.html")]
        return f"{BASE_URL}/{folder}/"

    # Any other html
    if rel.endswith(".html"):
        return f"{BASE_URL}/{rel[:-5]}"

    return f"{BASE_URL}/{rel}"


def _self_prefixes(desired: str) -> set[str]:
    # Treat trailing slash differences as self-candidate
    d = desired
    if d.endswith("/") and d != f"{BASE_URL}/":
        return {d, d[:-1]}
    return {d, d + "/"}


def _pick_canonical(existing: list[str], desired: str) -> str:
    if not existing:
        return desired

    desired_prefixes = _self_prefixes(desired)

    # If any canonical points elsewhere (not a self-candidate), keep the first one.
    # This preserves intentional canonicalisation while removing duplicates.
    for href in existing:
        if href and href not in desired_prefixes and not any(href.startswith(p) for p in desired_prefixes):
            return href

    # Otherwise normalize to desired
    return desired


def _remove_all_canonicals(html: str) -> str:
    return CANONICAL_RE.sub("", html)


def _ensure_single_canonical_in_head(html: str, canonical_href: str) -> str:
    lower = html.lower()
    head_end = lower.find("</head>")
    if head_end == -1:
        return html

    canonical_tag = f'<link rel="canonical" href="{canonical_href}">'  # keep existing style (no / >)

    return html[:head_end] + canonical_tag + "\n" + html[head_end:]


def _fix_services_breadcrumb_link(html: str) -> str:
    # Normalize the breadcrumb backlink to the canonical services URL (no .html)
    return html.replace('href="/services.html"', 'href="/services"')


def fix_public_pages(base_dir: Path) -> dict:
    service_pages = sorted((base_dir / "services").glob("*/index.html"))
    root_pages = [
        base_dir / "index.html",
        base_dir / "about.html",
        base_dir / "contact.html",
        base_dir / "services.html",
        base_dir / "privacy-policy.html",
        base_dir / "referrals.html",
        base_dir / "sitemap.html",
        base_dir / "service-area.html",
    ]

    targets = [p for p in root_pages if p.exists()] + [p for p in service_pages if p.exists()]

    backup_dir = base_dir / f"backup_public_canonicals_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    changed = []
    skipped = []
    errors = []

    for p in targets:
        try:
            html = p.read_text(encoding="utf-8", errors="ignore")
            original = html

            desired = _desired_canonical_for(p, base_dir)

            existing_tags = CANONICAL_RE.findall(html)
            existing_hrefs = [h for h in (_extract_href(t) for t in existing_tags) if h]
            chosen = _pick_canonical(existing_hrefs, desired)

            # Remove all canonicals (in/out of head), reinsert one into head
            html = _remove_all_canonicals(html)
            html = _ensure_single_canonical_in_head(html, chosen)

            # Backlink cleanup on service pages (breadcrumbs)
            if str(p.relative_to(base_dir)).replace("\\", "/").startswith("services/"):
                html = _fix_services_breadcrumb_link(html)

            if html != original:
                backup_path = backup_dir / p.relative_to(base_dir)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(original, encoding="utf-8")

                p.write_text(html, encoding="utf-8")
                changed.append(str(p.relative_to(base_dir)))
            else:
                skipped.append(str(p.relative_to(base_dir)))

        except Exception as e:
            errors.append(f"{p}: {e}")

    return {
        "targets": len(targets),
        "changed": changed,
        "skipped": skipped,
        "errors": errors,
        "backup_dir": str(backup_dir),
    }


if __name__ == "__main__":
    base = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec")
    res = fix_public_pages(base)
    print(f"Targets: {res['targets']}")
    print(f"Changed: {len(res['changed'])}")
    print(f"Skipped: {len(res['skipped'])}")
    print(f"Errors: {len(res['errors'])}")
    print(f"Backup: {res['backup_dir']}")
    if res["errors"]:
        print("Errors:\n" + "\n".join(res["errors"]))
