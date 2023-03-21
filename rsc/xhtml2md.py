from links import convert_links_to_md
import re, bs4

JUSTIFY_TAG = '<style type="text/css">p{text-align:justify;}</style>'
MD_SYNTAX = {
  "i": "_",
  "b": "**",
  "strike": "~~",
  "span": ""
}

def body2md(body: bs4.element.Tag, link_suffix: bool) -> str:
  convert_links_to_md(body, link_suffix)
  out = JUSTIFY_TAG + "\n\n# " + body.contents[0].get_text() + "\n"
  divs = [div2md(div) for div in body.contents[1:]]
  out += "\n\n".join(divs)
  return out

def div2md(div: bs4.element.Tag, min_out_h: int=2, min_in_h: int=3) -> str:
  out = ""
  for p in div.children:
    if p.name.startswith("h"):
      n = int(p.name[1])
      n = n - min_in_h + min_out_h
      out += "\n" + "#" * n + " "

    else:
      out += "\n\n"
      assert p.name == "p"

    out += p2md(p)
  out = flatten_quotes(out)
  return out.lstrip()

def p2md(p: bs4.element.Tag) -> str:
  handle_css(p)
  for descendant in p.find_all(True, style=True):
    handle_css(descendant)

  for tag_name, symbol in MD_SYNTAX.items():
    for child in p.find_all(tag_name):
      child.insert(0, symbol)
      child.append(symbol)
      child.unwrap()

  if len(p.find_all(True)) > 0:
    raise Exception("Unconverted tags in p", p.find_all(True))

  return p.get_text()

def handle_css(tag: bs4.element.Tag) -> None:
  if "style" not in tag.attrs:
    return
  for style in [style for style in tag["style"].strip(";").split(";")]:
    if style.startswith("text-align:") or style.startswith("margin-left:"):
      tag.insert(0, "> ")

def flatten_quotes(md: str) -> str:
  n = 1
  while n > 0:
    md, n = re.compile(r">([^\n]+)\n\n>").subn(">\\1  \n>", md)
  
  return md