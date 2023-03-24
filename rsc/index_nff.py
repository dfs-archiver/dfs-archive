from index_pl import get_body
import links
from pathlib import Path
import bs4, re

INDEX_HTML0 = Path("www.itsdougholland.com/p/movies.html").resolve(True)
ENTRY_RE = re.compile(r"#(\d{1,3})")

def generate_index(index_html0: Path):
  index_html = index_html0.read_text(encoding="utf-8")
  soup = bs4.BeautifulSoup(index_html, "html.parser")
  body = get_body(soup)
  entries = []
  for a in body.find_all("a"):
    text = a.get_text().strip()
    match = ENTRY_RE.match(text)
    if not match:
      continue

    entry_number = int(match.group(1))
    if entry_number != len(entries) + 1:
      raise Exception("Entry number mismatch", entry_number, len(entries) + 1)

    href = links.resolve(index_html0, a["href"])

    # link is wrong on the website
    if entry_number == 6:
      href = links.resolve(index_html0, "../2021/08/SevenMoreMovies.html")

    if href in entries:
      raise Exception("Duplicate entry", href)

    entries.append(href)
  
  return entries

INDEX_NFF = generate_index(INDEX_HTML0)