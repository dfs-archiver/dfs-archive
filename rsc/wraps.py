from nodes import format_str
import re, bs4

# easier to code if only first 3 chars matter
PROPERTY_ORDER = {
  "tag": 0,
  "lin": 1,
  "sty": 2
}

def wrap(paragraph):
  soup = bs4.BeautifulSoup()
  if paragraph[0][1].name.startswith("h"):
    p = soup.new_tag(paragraph[0][1].name)
  else:
    p = soup.new_tag("p")
  soup.append(p)

  wrapped = []
  for node in paragraph:
    wrapped.append(bs4.element.NavigableString(format_str(node[0].string)))
  # at this point, wrapped is just
  # [nav_str1, nav_str2, nav_str3, nav_str4, nav_str5]

  wraps = get_possible_wraps(paragraph)

  for property, wrap_start, wrap_len in wraps:
    # create the right tag for that wrap
    if property.startswith("tag-"):
      tag = soup.new_tag(property[4:])
    elif property.startswith("link-"):
      href = property[5:]
      tag = soup.new_tag("a", href=href)
    elif property.startswith("style-"):
      style = property[6:]
      tag = soup.new_tag("span", style=style)
    else:
      raise Exception("Unknown property", property)

    for j in range(wrap_start, wrap_start + wrap_len):
      # add all nav_strings or tags to that new tag
      tag.append(wrapped[j])
      # replace the nav_string/tag in the array
      wrapped[j] = tag

  # wrapped should look something like this:
  # [nav_str1, tag1, tag1, tag2, nav_string5]
  
  for tag in wrapped:
    p.append(tag)
  
  return p.extract()

def get_possible_wraps(paragraph):
  properties = []
  for node in paragraph:
    for property in node[2]:
      if property not in properties:
        properties.append(property)
  
  wraps = []
  for property in properties:
    i = 0
    while i < len(paragraph):
      wrap_start = i
      wrap_len = 0
      while i < len(paragraph) and has_property(paragraph[i], property, wrap_len):
        wrap_len += 1
        i += 1
      if wrap_len > 0:
        wraps.append((property, wrap_start, wrap_len))
      i += 1

  # sort by secondary order first
  wraps.sort(key = lambda wrap : PROPERTY_ORDER[wrap[0][:3]])

  # stable sort by primary order (wrap_len)
  wraps.sort(key = lambda wrap : wrap[2])
  
  return wraps

def has_property(node, property, wrap_len: int):
  if property in node[2]:
    return True
  # only be greedy when wrap already started
  if wrap_len == 0:
    return False
  # only whitespace: tag-i and tag-b don't matter
  # for any css style in the whitelist, whitespace doesn't matter either
  if (property == "tag-b" or property.startswith("style-")) and re.compile(r"\s+$").match(node[0].get_text()):
    return True
  if property == "tag-i" and re.compile(r"[\s\.:!?]+$").match(node[0].get_text()):
    return True
  
  return False