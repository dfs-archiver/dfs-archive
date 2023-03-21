import sys
sys.path.append("./rsc/")
from links import is_url, relative_to
from pathlib import Path
import pickle
import bs4

def convert_links(files: list[Path], link_list: dict[Path, tuple[str, str]]) -> int:
  i = 0
  for file in files:
    soup = bs4.BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
    for a in soup.find_all("a"):
      href = a["href"]
      if is_url(href):
        continue

      href = Path(href)
      
      if href not in link_list:
        a.unwrap()
        print("Could not find a converted link for href", href)
        continue
      
      href = relative_to(file, link_list[href])
      a["href"] = href
      i += 1

    file.write_text(str(soup), encoding="utf-8")

  return i

if __name__ == "__main__":
  with open("link_list.pkl", "rb") as f:
    link_list = pickle.load(f)
  with open("new_files.pkl", "rb") as f:
    files = pickle.load(f)
  n = convert_links(files, link_list)
  print("Converted", n, "links")