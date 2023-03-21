from pathlib import Path
import re, bs4

# Regex to remove all characters that are not allowed in github anchors
# No uppercase characters, they should already be converted before regex is used
ANCHOR_REMOVE = re.compile("[^a-zäöü0-9_\\- ]")
URL = re.compile(r"https?://|www\.")

"""
github-markup automatically creates anchors for headers.
However, this generation is not officially defined in the GFM specification (https://github.github.com/gfm/).
The only official documentation I found is here (step 4): 
https://github.com/github/markup/blob/b2230a29592f84e459a5278275fa4da8b9a57289/README.md#github-markup
This doesn't specify how exactly the anchors are generated though. More info: 
https://stackoverflow.com/a/72538392
"""

# Generates a github style anchor for a header
def generate_anchor_str(content: str) -> str:
  return ANCHOR_REMOVE.subn("", content.lower())[0].replace(" ", "-").strip("-")

def insert_anchor(soup: bs4.element.Tag) -> str:
  header = soup.find_all("h3")
  assert(len(header) == 1)
  header = header[0]
  anchor_str = generate_anchor_str(header.get_text())
  header["id"] = anchor_str
  return anchor_str

def resolve(file0: str, href: str) -> Path:
  # get absolute path of file0
  path = Path(file0).resolve(True)
  assert(path.is_file())
  # concatenate parent directory with href
  path = path.parent / href
  # resolve relative paths ("../")
  path = path.resolve(True)
  assert(path.is_file())
  return path

def convert_links_absolute(soup: bs4.element.Tag, file0: Path) -> int:
  i = 0
  for link in soup.find_all("a"):
    href = link["href"]
    if is_url(href):
      continue
    path = resolve(file0, href)
    link["href"] = str(path)
    i += 1
  return i

def is_url(href: str) -> bool:
  return URL.match(href) != None

def relative_to(file0: Path, href: tuple[Path, str]) -> str:
  path, anchor = href
  anchor = "#" + anchor if anchor else ""
  return path.relative_to(file0.parent).as_posix() +  anchor

def convert_links_to_md(soup: bs4.element.Tag, suffix: bool) -> None:
  for a in soup.find_all("a"):
    href = href2md(a["href"], suffix)
    a.insert(0, "[")
    a.append(f"]({href})")
    a.unwrap()

def href2md(href: str, suffix: bool) -> str:
  if is_url(href):
    return href
  suffix = ".md" if suffix else ""
  return href.replace(".xhtml", suffix)