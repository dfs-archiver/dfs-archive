import re, bs4

def smooth(soup: bs4.element.Tag) -> bs4.element.Tag:
  join_headers(soup)
  flatten_spans(soup)
  shift_whitespace(soup)
  remove_trailing_whitespace(soup)
  soup.smooth()
  return soup

def join_headers(soup: bs4.element.Tag) -> bs4.element.Tag:
  children = soup.contents
  for i in range(len(children) - 1):
    cur_tag = children[i].name
    next_tag = children[i + 1].name
    # both tags are headers
    if cur_tag.startswith("h") and cur_tag == next_tag:
      # move all children of next header to current header
      for child in children[i + 1].children:
        child.extract()
        children[i].append(child)
      # remove empty next header
      children[i + 1].decompose()
      # recursively call function again, because the next header may also be a header
      join_headers(soup)
      break
  
  return soup

def flatten_spans(soup: bs4.element.Tag) -> bs4.element.Tag:
  for span in soup.find_all("span"):
    # span is the only child of its parent
    if len(span.parent.contents) == 1:
      style = span.parent["style"] if "style" in span.parent.attrs else ""
      span.parent["style"] = style + span["style"]
      span.unwrap()
      # may be nested spans, so call function again
      flatten_spans(soup)
      break
  
  return soup

def shift_whitespace(soup: bs4.element.Tag) -> None:
  for nav_string in soup.strings:
    parent = nav_string.parent
    # if parent is a paragraph, don't shift whitespace
    if re.compile(r"p$|div$|h[1-6]$").match(parent.name):
      continue
    
    match = re.compile(r"^\s+|\s+$").match(parent.get_text())
    if not match:
      continue
    left = match.start() == 0
    stripped = 0
    to_strip = len(match.group(0))
    i = 0
    if left:
      parent.insert_before(match.group(0))
      while stripped < to_strip:
        obj = list(parent.strings)[i]
        before = len(obj)
        obj.replace_with(obj.lstrip())
        stripped += before - len(list(parent.strings)[i])
        i += 1
    else:
      parent.insert_after(match.group(0))
      while stripped < to_strip:
        obj = list(parent.strings)[-1 - i]
        before = len(obj)
        obj.replace_with(obj.rstrip())
        stripped += before - len(list(parent.strings)[-1 - i])
        i += 1
    
    # recursively call function again, because the whitespace may have been shifted
    # out of a nested tag, it has to be shifted until it's in a p tag
    shift_whitespace(soup)
    break

  # remove tags that are now empty
  [tag.decompose() for tag in soup.find_all(True) if tag.get_text() == ""]

def remove_trailing_whitespace(soup: bs4.element.Tag) -> bs4.element.Tag:
  remove = []
  for p in soup.children:
    nav_strings = list(p.find_all(string=True))
    for i in range(len(nav_strings)):
      left = nav_strings[i]
      parent = left.parent
      new = bs4.NavigableString(left.lstrip())
      left.replace_with(new)
      nav_strings[i] = new
      if len(new) > 0:
        break
      elif parent.get_text() == "":
        remove.append(parent)
    
    for right in nav_strings[::-1]:
      parent = right.parent
      new = right.rstrip()
      right.replace_with(new)
      if len(new) > 0:
        break
      elif parent.get_text() == "":
        remove.append(parent)
    
  for r in remove:
    r.decompose()
      
  return soup
