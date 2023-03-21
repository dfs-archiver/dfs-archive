import sys
sys.path.append("./rsc/")
from xhtml2md import body2md
from pathlib import Path
import os, bs4

def xhtml_dir_to_md(dir_in: Path, dir_out: Path, link_suffix: bool):
  for root, _, files in os.walk(dir_in):
    root = Path(root)
    out_dir = dir_out / root.relative_to(dir_in)
    out_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
      if not file.endswith(".xhtml"):
        continue
      file = root / file
      outfile = out_dir / file.with_suffix(".md").name
      soup = bs4.BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
      md = body2md(soup.body, link_suffix)
      outfile.write_text(md, encoding="utf-8")
      print("Converted", file, "to", outfile)

def main():
  xhtml_dir_to_md(Path("./out/xhtml/"), Path("./out/md/"), False)

if __name__ == "__main__":
  main()