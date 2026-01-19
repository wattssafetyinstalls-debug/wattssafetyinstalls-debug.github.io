#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path


def _extract_service_name(html: str, fallback: str) -> str:
    m = re.search(r'<h1[^>]*class="service-title"[^>]*>(.*?)</h1>', html, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() or fallback

    m = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if m:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if "|" in title:
            title = title.split("|")[0].strip()
        return title or fallback

    return fallback


def add_breadcrumbs_to_service_pages(base_dir: Path) -> dict:
    services_dir = base_dir / "services"
    service_pages = sorted(p for p in services_dir.glob("*/index.html") if p.is_file())

    backup_dir = base_dir / f"backup_service_breadcrumbs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    changed = []
    skipped = []
    errors = []

    breadcrumb_css = (
        "\n"
        ".breadcrumb {\n"
        "    background: var(--white, #FFFFFF);\n"
        "    padding: 20px 0;\n"
        "    box-shadow: 0 2px 10px rgba(0,0,0,0.05);\n"
        "}\n"
        "\n"
        ".breadcrumb-container {\n"
        "    max-width: 1300px;\n"
        "    margin: 0 auto;\n"
        "    padding: 0 20px;\n"
        "}\n"
        "\n"
        ".breadcrumb a {\n"
        "    color: var(--gray, #64748B);\n"
        "    text-decoration: none;\n"
        "    transition: color 0.3s;\n"
        "}\n"
        "\n"
        ".breadcrumb a:hover {\n"
        "    color: var(--teal, #00C4B4);\n"
        "}\n"
        "\n"
        ".breadcrumb span {\n"
        "    color: var(--navy, #0A1D37);\n"
        "    font-weight: 600;\n"
        "}\n"
        "\n"
        ".breadcrumb i {\n"
        "    margin: 0 10px;\n"
        "    color: var(--gray, #64748B);\n"
        "}\n"
        "\n"
        "@media (max-width: 768px) {\n"
        "    .breadcrumb {\n"
        "        padding: 15px 0;\n"
        "    }\n"
        "\n"
        "    .breadcrumb-container {\n"
        "        padding: 0 15px;\n"
        "    }\n"
        "\n"
        "    .breadcrumb i {\n"
        "        margin: 0 5px;\n"
        "        font-size: 0.8rem;\n"
        "    }\n"
        "}\n"
    )

    for page_path in service_pages:
        try:
            html = page_path.read_text(encoding="utf-8", errors="ignore")

            if 'class="breadcrumb"' in html or ".breadcrumb" in html:
                skipped.append(str(page_path.relative_to(base_dir)))
                continue

            service_name = _extract_service_name(html, fallback=page_path.parent.name.replace("-", " ").title())

            header_end = html.find("</header>")
            if header_end == -1:
                skipped.append(str(page_path.relative_to(base_dir)))
                continue

            breadcrumb_html = (
                "\n<div class=\"breadcrumb\">\n"
                "<div class=\"breadcrumb-container\">\n"
                "<a href=\"/\">Home</a>\n"
                "<i class=\"fas fa-chevron-right\"></i>\n"
                "<a href=\"/services.html\">Services</a>\n"
                "<i class=\"fas fa-chevron-right\"></i>\n"
                f"<span>{service_name}</span>\n"
                "</div>\n"
                "</div>\n"
            )

            insert_pos = header_end + len("</header>")
            html2 = html[:insert_pos] + breadcrumb_html + html[insert_pos:]

            # Inject CSS into <head> safely (never append raw CSS at EOF)
            if ".breadcrumb" not in html:
                lower = html2.lower()
                head_end = lower.find("</head>")
                if head_end == -1:
                    skipped.append(str(page_path.relative_to(base_dir)))
                    continue

                style_end = lower.find("</style>")
                if style_end != -1 and style_end < head_end:
                    html2 = html2[:style_end] + breadcrumb_css + html2[style_end:]
                else:
                    html2 = html2[:head_end] + "<style>" + breadcrumb_css + "</style>\n" + html2[head_end:]

            if html2 != html:
                # Backup before write
                backup_path = backup_dir / page_path.relative_to(base_dir)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(html, encoding="utf-8")

                page_path.write_text(html2, encoding="utf-8")
                changed.append(str(page_path.relative_to(base_dir)))
            else:
                skipped.append(str(page_path.relative_to(base_dir)))

        except Exception as e:
            errors.append(f"{page_path}: {e}")

    return {
        "backup_dir": str(backup_dir),
        "changed": changed,
        "skipped": skipped,
        "errors": errors,
        "total": len(service_pages),
    }


if __name__ == "__main__":
    base = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec")
    result = add_breadcrumbs_to_service_pages(base)
    print(f"Total service pages found: {result['total']}")
    print(f"Updated: {len(result['changed'])}")
    print(f"Skipped: {len(result['skipped'])}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Backup: {result['backup_dir']}")
    if result["errors"]:
        print("Errors:\n" + "\n".join(result["errors"]))
