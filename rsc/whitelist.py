import re

# TODO: tag whitelist?

ATTR_WHITELIST = re.compile(
  r"style$|"
  r"align$"
)

CSS_WHITELIST = re.compile(
  r"text-align:(?:center|right);$|"
  r"margin-left:(?:40px|80px|120px);$|"
  r"font-family:(?:courier|Calibri);$|"
  r"color:"
)

def validate_attrs(attrs: dict[str, str]):
  for key in attrs:
    if not ATTR_WHITELIST.search(key):
      raise Exception("Unrecognized attribute", key)

def validate_css(styles: list[str]):
  for style in styles:
    if not CSS_WHITELIST.search(style):
      raise Exception("Unrecognized style", style)