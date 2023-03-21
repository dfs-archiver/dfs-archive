import re
from bs4.element import Tag

REMOVE = re.compile(
  r"^This is an entry retyped from an on-paper zine.+Pathetic Life|"
  r"^Pathetic Life$|"
  r"^PATHETIC LIFE$|"
  r"^← PREVIOUS\s*NEXT →|"
  r"^NEXT →|"
  r"^itsdougholland.com$|"
  r"^Next: Part|"
  r"^Part 1 •|"
  r"^From Pathetic Life #\d\d?$"
)

def clean_contents(soup: Tag) -> Tag:
  # gather all paragraphs that should be removed first
  # else there are unexpected results when removing them
  remove_me = [p for p in soup.children if REMOVE.search(p.get_text())]
  for p in remove_me:
    p.decompose()