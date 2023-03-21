from copy import deepcopy
from bs4 import BeautifulSoup

_SKEL0 = "./rsc/skel.xhtml"
with open(_SKEL0, "r", encoding="utf-8") as f:
  _SKEL_STR = f.read()
_SKEL = BeautifulSoup(_SKEL_STR, "html.parser")

# returns a copy of the xhtml skeleton
def xhtml() -> BeautifulSoup:
  return deepcopy(_SKEL)