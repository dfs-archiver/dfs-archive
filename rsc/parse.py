from nodes import get_nodes
from paragraphs import pack_into_paragraphs
from xhtml import xhtml
from wraps import wrap
from smooth import smooth
import bs4

# same as parse_soup but operates on file
def parse_file(file0: str) -> bs4.BeautifulSoup:
  with open(file0, "r", encoding="utf-8") as f:
    data = f.read()
  
  soup = bs4.BeautifulSoup(data, "html.parser")
  return parse_soup(soup)

def parse_soup(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
  post = get_post(soup)
  # TODO: what to do with images?
  nodes = get_nodes(post, False)
  paragraphs = pack_into_paragraphs(nodes)
  out = xhtml()
  for paragraph in paragraphs:
    p = wrap(paragraph)
    out.body.append(p)
  
  smooth(out.body)

  return out

# (safely) get the post element from the soup
def get_post(soup: bs4.BeautifulSoup) -> bs4.element.Tag:
  posts = soup.find_all(itemprop="blogPost")
  if len(posts) != 1:
    raise Exception("Expected exactly one post but got", len(posts))
  return posts[0]

def leading_zero(n: int, max: int=2):
  n = str(n)
  return "0" * (max - len(n)) + n