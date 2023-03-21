import re, bs4

def pack_into_paragraphs(nodes: list[(bs4.element.Tag, list)]):
  paragraphs = []
  # current paragraph
  # init value is a dummy paragraph, that always returns False for is_same_p
  # because cur_p[-1][1] is []
  # and [] *is not* any other paragraph (is operator checks for memory address equality)
  cur_p = [(None, [])]
  for node in nodes:
    # last element of cur_p and node belong to same paragraph
    if is_same_p(cur_p[-1], node):
      cur_p.append(node)
    else:
      # start new paragraph
      cur_p = [node]
      # add cur_p to paragraphs
      paragraphs.append(cur_p)
  
  return paragraphs

def is_same_p(node1: tuple[bs4.element.Tag, list], node2: tuple[bs4.element.Tag, list]) -> bool:
  # don't even belong to same paragraph
  if node1[1] is not node2[1]:
    return False
  # may belong to same paragraph, but there may be a linebreak between them
  return not is_linebreak_between(node1[1], node1[0], node2[0])
  
def is_linebreak_between(paragraph: bs4.element.Tag, start: bs4.element.Tag, end: bs4.element.Tag) -> bool:
  between = False
  for descendant in paragraph.descendants:
    # no linebreak found, exit loop
    if descendant is end:
      break
    # start node reached, start looking for linebreaks
    elif descendant is start:
      between = True
      continue
    if not between:
      continue
    if type(descendant) == bs4.element.Tag and re.compile(r"p$|div$|h[1-6]$|br$").match(descendant.name):
      return True
    
  return False