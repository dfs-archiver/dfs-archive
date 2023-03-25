from pathlib import Path

DIR = Path("./out/md/").resolve(True)
BASE_URL = "/dfs-archiver/dfs-archive/wiki/"

def dir2sidebar(dir: Path) -> str:
  files = [file.stem for file in dir.iterdir() if file.is_file() and file.suffix == ".md" and file.name != "_Sidebar.md"]
  files.sort()

  mds = []
  for name in files:
    href = BASE_URL + name
    md = f"  * [{name}]({href})"
    mds.append(md)

  return "\n".join(mds)

# inserts a new line after the line containing series
def insert(base: str, series: str, text: str) -> str:
  lines = base.split("\n")
  i = 0
  while series not in lines[i]:
    i += 1
  lines.insert(i + 1, text)
  return "\n".join(lines)

def main():
  base_sidebar0 = DIR / "_Sidebar.md"
  base_sidebar = base_sidebar0.read_text()
  for dir in DIR.iterdir():
    if not dir.is_dir() or dir.name.startswith("."):
      continue

    sidebar = dir2sidebar(dir)
    md = insert(base_sidebar, dir.name, sidebar)

    sidebar0 = dir / "_Sidebar.md"
    sidebar0.write_text(md)
    print("Wrote", sidebar0)

if __name__ == "__main__":
  main()