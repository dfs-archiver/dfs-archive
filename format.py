import sys
sys.path.append("./rsc/")
sys.path.append("./rsc/formatting/")
from index_pl import INDEX_PL
from index_bad import INDEX_BAD
from index_cof import INDEX_COF
from index_nff import INDEX_NFF
from get_html_files import get_html_files
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

def add_header(soup: bs4.BeautifulSoup, header: str) -> bs4.element.Tag:
  tag = soup.new_tag("h2")
  tag.string = header
  soup.body.append(tag)
  return tag

def format_pl_files():
  PL_DIR = OUT_DIR0 / "Pathetic Life/"
  for issue_number, issue in INDEX_PL.items():
    out0 = PL_DIR / f"PL-{leading_zero(issue_number)}.xhtml"

    issue_soup = xhtml()
    title = f"Pathetic Life #{issue_number}"
    add_title_tag(issue_soup, title)
    add_header(issue_soup, title)
    for entry in issue["entries"]:
      href = entry["href"]
      try:
        entry_soup = parse_file(href)
        format_pl(entry_soup, entry_soup.body)
        clean_contents(entry_soup.body)
        anchor = insert_anchor(entry_soup)
        convert_links_absolute(entry_soup, href)
        
        # create div for entry
        div = issue_soup.new_tag("div")
        issue_soup.body.append(div)
        # add entry to issue_soup
        body = entry_soup.body.extract()
        div.append(body)
        body.unwrap()

        link_list[href] = (out0, anchor)
      except Exception as e:
        print("Error while parsing", href, e)
        continue

    new_files.append(out0)
    out0.write_text(str(issue_soup), encoding="utf-8")
    print("Wrote", out0.name)

def format_bad_files():
  BAD_DIR = OUT_DIR0 / "Breakfast at the Diner/"
  for i in range(len(INDEX_BAD)):
    issue_number = i + 1
    href = INDEX_BAD[i]
    out0 = BAD_DIR / f"BAD-{leading_zero(issue_number, 3)}.xhtml"
    soup = xhtml()
    title = f"Breakfast at the Diner #{issue_number}"
    add_title_tag(soup, title)

    try:
      entry_soup = parse_file(href)
      # format_bad(entry_soup, entry_soup.body)
      clean_contents(entry_soup.body)
      # anchor = insert_anchor(entry_soup)
      convert_links_absolute(entry_soup, href)

      header_old = entry_soup.find("h3").extract()
      header_new = soup.new_tag("h2")
      header_new.append(header_old)
      soup.body.append(header_new)
      header_old.unwrap()

      div = soup.new_tag("div")
      soup.body.append(div)
      body = entry_soup.body.extract()
      div.append(body)
      body.unwrap()

      # anchor?
      link_list[href] = (out0, None)
      new_files.append(out0)
      out0.write_text(str(soup), encoding="utf-8")
      print("Wrote", out0.name)
    except Exception as e:
      print("Error while parsing", href, e)
      continue

def format_cof_files():
  COF_DIR = OUT_DIR0 / "Cranky Old Fart/"
  for i in range(len(INDEX_COF)):
    entry_number = i + 1
    href = INDEX_COF[i]
    out0 = COF_DIR / f"COF-{leading_zero(entry_number, 3)}.xhtml"
    soup = xhtml()

    try:
      entry_soup = parse_file(href)
      # format_cof(entry_soup, entry_soup.body)
      clean_contents(entry_soup.body)
      # anchor = insert_anchor(entry_soup)
      convert_links_absolute(entry_soup, href)

      header_old = entry_soup.find("h3").extract()
      header_text = header_old.get_text().strip()
      header_new = soup.new_tag("h2")
      header_new.append(header_old)
      soup.body.append(header_new)
      header_old.unwrap()

      title = f"Cranky Old Fart #{entry_number}: {header_text}"
      add_title_tag(soup, title)

      div = soup.new_tag("div")
      soup.body.append(div)
      body = entry_soup.body.extract()
      div.append(body)
      body.unwrap()

      link_list[href] = (out0, None)
      new_files.append(out0)
      out0.write_text(str(soup), encoding="utf-8")
      print("Wrote", out0.name)
    except Exception as e:
      print("Error while parsing", href, e)
      continue

def format_nff_files():
  NFF_DIR = OUT_DIR0 / "Neverending Film Festival/"
  for i in range(len(INDEX_NFF)):
    entry_number = i + 1
    href = INDEX_NFF[i]
    out0 = NFF_DIR / f"NFF-{leading_zero(entry_number, 3)}.xhtml"
    soup = xhtml()
    title = f"Neverending Film Festival #{entry_number}"
    add_title_tag(soup, title)

    try:
      entry_soup = parse_file(href)
      # format_nff(entry_soup, entry_soup.body)
      clean_contents(entry_soup.body)
      # anchor = insert_anchor(entry_soup)
      convert_links_absolute(entry_soup, href)

      header_old = entry_soup.find("h3").extract()
      header_new = soup.new_tag("h2")
      header_new.append(header_old)
      soup.body.append(header_new)
      header_old.unwrap()

      div = soup.new_tag("div")
      soup.body.append(div)
      body = entry_soup.body.extract()
      div.append(body)
      body.unwrap()

      link_list[href] = (out0, None)
      new_files.append(out0)
      out0.write_text(str(soup), encoding="utf-8")
      print("Wrote", out0.name)
    except Exception as e:
      print("Error while parsing", href, e)
      continue

def format_misc_files(exclude_files: list[Path]):
  IN_DIR0 = Path("www.itsdougholland.com/").resolve(True)
  MISC_DIR = OUT_DIR0 / "Miscellaneous/"
  files = get_html_files(IN_DIR0, exclude_files)

  for i in range(len(files)):
    href = files[i]
    soup = xhtml()

    try:
      entry_soup = parse_file(href)
      # format_misc(entry_soup, entry_soup.body)
      clean_contents(entry_soup.body)
      # anchor = insert_anchor(entry_soup)
      convert_links_absolute(entry_soup, href)

      # special case for p/breakfast-at-diner.html: the title header was removed by clean_contents
      if href.name == "breakfast-at-diner.html":
        header = entry_soup.new_tag("h3")
        header.append("Breakfast at the Diner")
        entry_soup.body.insert(0, header)
      # same for p/ll.html
      elif href.name == "ll.html":
        header = entry_soup.new_tag("h3")
        header.append("Cranky Old Fart")
        entry_soup.body.insert(0, header)

      header_old = entry_soup.find("h3").extract()
      header_text = header_old.get_text().strip()
      header_new = soup.new_tag("h2")
      header_new.append(header_old)
      soup.body.append(header_new)
      header_old.unwrap()

      title = f"Diary of a Fat Slob: {header_text}"
      add_title_tag(soup, title)

      div = soup.new_tag("div")
      soup.body.append(div)
      body = entry_soup.body.extract()
      div.append(body)
      body.unwrap()

      file_name = "".join(c for c in header_text if c.isalnum() or c in " -_").strip().replace(" ", "-")
      file_name += ".xhtml"
      out0 = MISC_DIR / file_name

      link_list[href] = (out0, None)
      new_files.append(out0)
      out0.write_text(str(soup), encoding="utf-8")
      print("Wrote", out0.name)
    except Exception as e:
      print("Error while parsing", href, e)
      continue

def main():
  format_pl_files()
  format_bad_files()
  format_cof_files()
  format_nff_files()

  # backup 1
  with open("bak1.pkl", "wb") as f:
    pickle.dump((new_files, link_list), f)

  # load backup
  # with open("bak2.pkl", "rb") as f:
  #   new_files1, link_list1 = pickle.load(f)
  # new_files.extend(new_files1)
  # link_list.update(link_list1)

  converted_files = list(link_list.keys())
  format_misc_files(converted_files)

  # backup 2
  with open("bak2.pkl", "wb") as f:
    pickle.dump((new_files, link_list), f)

  n = convert_links(new_files, link_list)
  print("Converted", n, "links")

if __name__ == "__main__":
  main()