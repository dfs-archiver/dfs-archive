import css_styles, re, bs4

PROPERTY_TAGS = ["i", "b", "strike"]

# gets only important nodes from the soup
def get_nodes(soup: bs4.element.Tag, include_images: bool=True) -> list[(bs4.element.Tag, bs4.element.Tag, list[str])]:
  nodes = []
  for descendant in soup.descendants:
    t = node_type(descendant)
    if include_node(descendant, include_images):
      if t == 2:
        nodes.append((descendant, None))
      else:
        p, properties = determine_properties(descendant, soup)
        if properties == None:
          continue
        nodes.append((descendant, p, properties))

  return nodes

def include_node(node, include_images: bool) -> bool:
  t = node_type(node)
  if t == 0:
    return False
  elif t == 1 and len(format_str(node)) == 0:
    return False
  elif t == 2 and not include_images:
    return False
  else:
    return True

# returns 1 for nav_string 2 for img and 0 for everything else
def node_type(node) -> int:
  if type(node) == bs4.element.NavigableString:
    return 1
  elif type(node) in (bs4.element.Stylesheet, bs4.element.Script):
    return 0
  elif type(node) != bs4.element.Tag:
    raise Exception("Expected node to be a Tag or NavigableString but got", type(node))
  elif node.name == "img":
    return 2
  else:
    return 0

def format_str(s: str) -> str:
  return re.subn(r"\s+", " ", s)[0]

# returns a list of properties for the string, with the first element being the paragraph
# provide a parent for better performance but less accuracy
# returns None if string should be excluded
def determine_properties(nav_string: bs4.element.NavigableString, parent: bs4.element.Tag=None) -> list:
  properties = []
  p = None
  tag = nav_string.parent
  # DEBUG
  parent = None
  while tag != None and tag != parent:
    # should only be part of td when it's used as an image description
    if tag.name == "td":
      return None, None
    # self describing tags
    if tag.name in PROPERTY_TAGS and tag.name not in properties:
      properties.append("tag-" + tag.name)
    # links
    elif tag.name == "a":
      properties.append("link-" + tag["href"])
    # blockquotes
    elif tag.name == "blockquote":
      properties.append("style-margin-left:40px;")
    # paragraphs
    elif re.compile(r"p$|div$|h[1-6]$").match(tag.name) and p == None:
      p = tag

    # handle attributes, including css styles
    styles = css_styles.generate(tag.attrs)
    for style in styles:
      style = "style-" + style
      if style not in properties:
        properties.append(style)

    tag = tag.parent

  return p, properties