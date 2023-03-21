import blacklist, whitelist

def generate(attrs: dict[str, str]) -> list[str]:
  attrs = blacklist.clean_attrs(attrs)
  whitelist.validate_attrs(attrs)
  for key, value in attrs.items():
    if key == "style":
      styles = blacklist.clean_css(value)
      whitelist.validate_css(styles)
      return styles

    if key == "align" and value == "center":
      return ["text-align:center"]

  return []