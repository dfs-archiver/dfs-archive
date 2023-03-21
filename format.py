import sys
sys.path.append("./rsc/")
sys.path.append("./rsc/formatting/")
from index_pl import INDEX_PL
from xhtml import xhtml
from parse import parse_file, leading_zero
from links import insert_anchor, convert_links_absolute
from format_pl import format_pl
from clean_contents import clean_contents
from convert_links import convert_links
from pathlib import Path
import pickle, bs4

OUT_DIR0 = Path("out/xhtml").resolve(True)
link_list = {}
new_files = []

def add_title_tag(soup: bs4.BeautifulSoup, title: str) -> bs4.element.Tag:
  tag = soup.new_tag("title")
  tag.string = title
  soup.head.append(tag)
  return tag

def add_style_tag(soup: bs4.BeautifulSoup) -> bs4.element.Tag:
  tag = soup.new_tag("style", type="text/css")
  tag.string = "p{text-align:justify;}"
  soup.head.append(tag)
  return tag

def add_header(soup: bs4.BeautifulSoup, header: str) -> bs4.element.Tag:
  tag = soup.new_tag("h2")
  tag.string = header
  soup.body.append(tag)
  return tag

def format_pl_files():
  PL_DIR = OUT_DIR0 / "Pathetic Life/"
  for issue_number, issue in INDEX_PL.items():
    out0 = PL_DIR / f"Issue-{leading_zero(issue_number)}.xhtml"

    issue_soup = xhtml()
    title = f"Pathetic Life #{issue_number}"
    add_title_tag(issue_soup, title)
    add_style_tag(issue_soup)
    add_header(issue_soup, title)
    for entry in issue["entries"]:
      href = entry["href"]
      try:
        entry_soup = parse_file(href)
        format_pl(entry_soup, entry_soup.body)
        clean_contents(entry_soup.body)
        anchor = insert_anchor(entry_soup)
        convert_links_absolute(entry_soup, href)
      except Exception as e:
        print("Error while parsing", href, e)
        continue

      # create div for entry
      div = issue_soup.new_tag("div")
      issue_soup.body.append(div)
      # add entry to issue_soup
      body = entry_soup.body.extract()
      div.append(body)
      body.unwrap()

      link_list[href] = (out0, anchor)

    new_files.append(out0)
    out0.write_text(str(issue_soup), encoding="utf-8")
    print("Wrote", out0.name)

def main():
  format_pl_files()
  with open("link_list.pkl", "wb") as f:
    pickle.dump(link_list, f)
  with open("new_files.pkl", "wb") as f:
    pickle.dump(new_files, f)
  n = convert_links(new_files, link_list)
  print("Converted", n, "links")

if __name__ == "__main__":
  main()