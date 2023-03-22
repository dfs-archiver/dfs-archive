from index_pl import get_body
import links
from pathlib import Path
import re, bs4

INDEX_HTML0 = Path("www.itsdougholland.com/p/breakfast-at-diner.html").resolve(True)
ENTRY_RE = re.compile(r"#(\d{1,3})")

def generate_index(index_html0: Path):
  index_html = index_html0.read_text(encoding="utf-8")
  soup = bs4.BeautifulSoup(index_html, "html.parser")
  body = get_body(soup)
  entries = []
  for a in soup.find_all("a"):
    match = ENTRY_RE.match(a.get_text())
    if not match:
      continue

    entry_number = int(match.group(1))
    if entry_number != len(entries) + 1:
      raise Exception("Entry number mismatch", entry_number, len(entries) + 1)
    href = links.resolve(index_html0, a["href"])
    entries.append(href)

  return entries

INDEX_BAD = generate_index(INDEX_HTML0)