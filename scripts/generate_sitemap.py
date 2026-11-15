
from pathlib import Path
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape

# Your website URL
BASE_URL = "https://rohitmaurya.co.in"

ROOT = Path(__file__).resolve().parent.parent

# Folders and files to ignore
IGNORE_DIRS = {
    ".git", ".github", "node_modules",
    "assets", "images", "css", "js"
}

# Find all HTML pages
pages = []

for file in ROOT.rglob("*.html"):
    relative = file.relative_to(ROOT)

    if any(part in IGNORE_DIRS for part in relative.parts):
        continue

    if file.name in {"sitemap.html", "404.html"}:
        continue

    if file.name == "index.html":
        url_path = ""
    else:
        url_path = relative.as_posix()

    url = f"{BASE_URL}/{url_path}"

    last_modified = datetime.fromtimestamp(
        file.stat().st_mtime,
        tz=timezone.utc
    ).date().isoformat()

    pages.append((url, last_modified))

pages.sort()

# Generate sitemap.xml
urlset = Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)

for url, lastmod in pages:
    item = SubElement(urlset, "url")
    SubElement(item, "loc").text = url
    SubElement(item, "lastmod").text = lastmod

ElementTree(urlset).write(
    ROOT / "sitemap.xml",
    encoding="utf-8",
    xml_declaration=True
)

# Generate sitemap.html
html_links = "\n".join(
    f'<li><a href="{escape(url)}">{escape(url)}</a></li>'
    for url, _ in pages
)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow">
  <title>HTML Sitemap | Rohit Maurya</title>
  <meta name="description"
        content="Browse all pages on Rohit Maurya's professional portfolio website.">
  <link rel="canonical"
        href="{BASE_URL}/sitemap.html">
</head>
<body>
  <h1>Website Sitemap</h1>
  <p>Explore all pages on Rohit Maurya's portfolio.</p>
  <ul>
    {html_links}
  </ul>
</body>
</html>
"""

(ROOT / "sitemap.html").write_text(
    html_content,
    encoding="utf-8"
)

print(f"Generated sitemap with {len(pages)} HTML pages.")
