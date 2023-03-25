from pathlib import Path

def get_html_files(dir0: Path, exclude_files: list[Path]=[]) -> list[Path]:
  return [path for path in dir0.rglob("*.html") if path.is_file() and path not in exclude_files]