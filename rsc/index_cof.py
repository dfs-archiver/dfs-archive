from index_pl import get_body
import links
from pathlib import Path
import bs4, re

INDEX_HTML0 = Path("www.itsdougholland.com/p/ll.html").resolve(True)
ENTRY_RE = re.compile(r"(\d{1,3})\.")

def generate_index(index_html0: Path):
  index_html = index_html0.read_text(encoding="utf-8")
  soup = bs4.BeautifulSoup(index_html, "html.parser")
  body = get_body(soup)
  entries = []
  a_tags = list(body.find_all("a"))[::-1]
  for a in a_tags:
    p = a.find_parent("p")
    a.extract()
    text = p.get_text().strip()
    match = ENTRY_RE.match(text)
    if not match:
      continue

    entry_number = int(match.group(1))
    if entry_number != len(entries) + 1:
      raise Exception("Entry number mismatch", entry_number, len(entries) + 1)

    href = links.resolve(index_html0, a["href"])

    if href in entries:
      raise Exception("Duplicate entry", href)

    entries.append(href)

  return entries

INDEX_COF = generate_index(INDEX_HTML0)
pass