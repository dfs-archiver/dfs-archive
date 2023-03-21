import os, re
from pathlib import Path
from shutil import rmtree

# TODO: rewrite, considering the new clone_website.sh script

SAFE_REMOVE = re.compile(r"@showComment")
REMOVE_DIRS = re.compile(r"^b$|^feeds$|^js$")
REMOVE_FILES = re.compile(
  r"^favicon\.ico$|"
  r"^robots\.txt$|"
  r"^index\.html$|"
  r"^archives\.html$|"
  r"^the-archives-20\d\d\.html$"
)

# only remove files that shouldn't be needed at all
def safe_clean_dir(dir: str) -> int:
  removed_files = 0
  for root, _, files in os.walk(dir):
    for file in files:
      if not SAFE_REMOVE.search(file):
        continue

      file = Path(root) / file
      file.unlink()
      removed_files += 1
  
  return removed_files

# removes all files that aren't needed for further processing
def clean_dir(dir: str) -> tuple[int, int]:
  removed_files = safe_clean_dir(dir)
  removed_dirs = 0
  for root, dirs, files in os.walk(dir):
    for dir0 in dirs:
      if not REMOVE_DIRS.search(dir0):
        continue
      dir = Path(root) / dir0
      rmtree(dir)
      # dirs.remove(dir0)
      removed_dirs += 1
    
    for file in files:
      if not REMOVE_FILES.search(file):
        continue
      file = Path(root) / file
      file.unlink()
      removed_files += 1

  return removed_files, removed_dirs

def main():
  removed_files, removed_dirs = clean_dir("./www.itsdougholland.com/")
  print(f"Removed {removed_files} files and {removed_dirs} directories.")

if __name__ == "__main__":
  main()