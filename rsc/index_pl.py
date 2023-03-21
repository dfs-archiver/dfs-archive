from parse import leading_zero
import links
from pathlib import Path
import re, bs4

INDEX_HTML0 = Path("www.itsdougholland.com/p/pathetic-life.html").resolve(True)
PARTS = {
  "①": 1,
  "②": 2,
  "③": 3,
  "④": 4
}
ENTRY_RE = re.compile(r"(\d\d?)\/(\d\d?)(?:-(\d\d?))?([①②③④])?")
ISSUE_RE = re.compile(r"Pathetic Life #(\d\d?) ?— [A-Z][a-z]+ 199[4-6]$")

def generate_index(index_html0: Path):
  with open(index_html0, "r", encoding="utf-8") as f:
    index_html = f.read()
  soup = bs4.BeautifulSoup(index_html, "html.parser")
  soup = get_body(soup)
  clean_soup(soup)
  link_list = []
  issues = {}
  for a in soup.find_all("a"):
    href = links.resolve(index_html0, a["href"])
    if href in link_list:
      raise Exception("Duplicate href", href)
    link_list.append(href)
    
    month, day_start, day_end, part = parse_entry_date(a.get_text())
    header = a.parent.contents[0]
    issue_number = parse_issue_number(header.get_text())
    issue_month, issue_year = get_issue_month_yeah(issue_number)
    if month != issue_month:
      raise Exception("Month mismatch", month, issue_month)
    if issue_number not in issues:
      issues[issue_number] = {
        "year": issue_year,
        "month": issue_month,
        "entries": []
      }

    issue = issues[issue_number]
    issue["entries"].append({
      "href": href,
      "month": month,
      "day_start": day_start,
      "day_end": day_end,
      "part": part
    })
  
  for _, issue in issues.items():
    issue["entries"].sort(key=lambda entry :
      leading_zero(entry["month"]) +
      leading_zero(entry["day_start"]) +
      leading_zero(entry["part"])
    )
  
  validate_issues_dry(issues)
  return issues

def get_body(soup: bs4.BeautifulSoup) -> bs4.element.Tag:
  body = soup.find_all(itemprop="description articleBody")
  if len(body) != 1:
    raise Exception("There should be exactly one body in index, found", len(body))

  return body[0]

# hard coded filters, it's easier to remove them before further steps
def clean_soup(soup: bs4.element.Tag):
  img_a = soup.find("img").parent
  if img_a.name != "a":
    raise Exception("Img should be in a", img_a.name)
  img_a.decompose()
  soup.find("a", string="cast of characters").decompose()
  soup.find("a", string="3/1/1995").decompose()
  soup.find("a", string="itsdougholland.com").decompose()
  soup.find("a", href="http://jffrymyr.com/").decompose()

  remove = soup.find_all(lambda tag: 
    safe_is_tag(tag, "a") and
    tag.get("href") == "../2021/07/100194.html" and
    len(tag.contents) == 1 and
    safe_is_tag(tag.contents[0], "br")
  )
  assert len(remove) == 3
  for r in remove:
    r.decompose()

  remove = soup.find_all(lambda tag: 
    safe_is_tag(tag, "a") and
    tag.get("href") == "../2023/01/distance-is-my-favorite-family-value.html" and
    len(tag.contents) == 1 and
    safe_is_tag(tag.contents[0], "br")
  )
  assert len(remove) == 2
  for r in remove:
    r.decompose()

# safely checks whether a tag is a tag with a given name
def safe_is_tag(tag: bs4.element.Tag, tag_name: str) -> bool:
  return type(tag) == bs4.element.Tag and tag.name == tag_name

# returns (month, day_start, day_end, part)
def parse_entry_date(s: str) -> tuple[int, int, int, int]:
  match = ENTRY_RE.match(s)
  if not match:
    raise Exception("Could not parse PL entry date", s)

  month = int(match.group(1))
  day_start = int(match.group(2))
  # day_end could be None, but that's fine, just don't parse it as an int :)
  day_end = int(match.group(3)) if match.group(3) else None
  part = match.group(4)
  # part could be None too
  if part:
    part = get_part(part)

  return (month, day_start, day_end, part)

def get_part(symbol: str) -> int:
  if symbol not in PARTS:
    raise Exception("Unknown part", symbol)
  return PARTS[symbol]

def parse_issue_number(s: str) -> int:
  match = ISSUE_RE.match(s)
  if not match:
    raise Exception("Could not parse PL issue number", s)
  return int(match.group(1))

# yeah mr white, get the issue month (and year)
def get_issue_month_yeah(issue):
  # first issue was published in june '94
  # (4 + 1) % 12 + 1 = 6
  # (4 + 8) % 12 + 1 = 1
  month = (4 + issue) % 12 + 1
  # (4 + 1) // 12 + 1994 = 1994
  # (4 + 8) // 12 + 1994 = 1994
  # (4 + 9) // 12 + 1994 = 1995
  year = (4 + issue) // 12 + 1994
  return (month, year)

def validate_issues_dry(issues: dict[int, dict]) -> None:
  # make sure no day was skipped
  day = 0
  month = 6
  part = 0

  for _, issue in issues.items():
    for entry in issue["entries"]:
      if entry["month"] != month:
        if entry["day_start"] != 1 or day < 28:
          raise Exception("Unexpected new month")
        month = month % 12 + 1
        # this issue was never published
        if month == 2 and issue["year"] == 1995:
          month += 1
        if month != entry["month"]:
          raise Exception("Unexpected month")
        day = 0
      
      skip_day_check = False
      if entry["part"] == None:
        part = 0
      else:
        if entry["part"] != part + 1:
          raise Exception("Unexpected part")
        # part 1 should be different day than part 0 (because part 0 doesn't exists, thats just the day before)
        # part 1, 2, 3, etc. should all be the same day
        if part != 0:
          skip_day_check = True
        part += 1
      
      # special case, two entries on the same day
      if issue["year"] == 1996 and month == 2 and entry["day_start"] == 29 and part == 1:
        day = 28
      
      if entry["day_start"] != day + 1 and not skip_day_check:
        raise Exception("Unexpected day start")
      day = entry["day_end"] if entry["day_end"] else entry["day_start"]

INDEX_PL = generate_index(INDEX_HTML0)