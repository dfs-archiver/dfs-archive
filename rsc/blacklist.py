import re

# TODO: tag blacklist?

ATTR_BLACKLIST = re.compile(
  r"^class$|"
  r"^lang$|"
  r"^id$|"
  r"^itemprop$|"
  r"^name$|"
  r"^itemtype$|"
  r"^itemscope$|"
  r"^data-version$|"
  r"^href$|"
  r"^xmlns|"
  r"^dir|"
  r"^face|"
  r"^title$|"
  r"^data-href-url$|"
  r"^data-blogger-escaped-$|"
  r"^rel$|"
  r"^target$|"
  r"^aria-level$|"
  r"^role$"
)

CSS_BLACKLIST = re.compile(
  r"^line-height:|"
  r"^margin-bottom:|"
  r"^font-size:|"
  r"^text-align:left;$|"
  r"^background:transparent|"
  r"^font-style:normal;$|"
  r"^color:black|"
  r"^clear:(?:both|right);$|"
  r"^font-family:inherit;$|"
  r"^font-weight:normal;$|"
  r"^margin-(?:left|right):1em;$|"
  r"^float:right;$"
)

def clean_attrs(attrs: dict[str, str]) -> dict[str, str]:
  return {key: value for key, value in attrs.items() if not ATTR_BLACKLIST.search(key)}

def clean_css(string: str) -> list[str]:
  styles = [style.replace(" ", "") + ";" for style in string.strip(";").split(";")]
  return [style for style in styles if not CSS_BLACKLIST.search(style)]