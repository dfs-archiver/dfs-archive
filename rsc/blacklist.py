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
  r"^role$|"
  r"^data-dobid$"
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
  r"^float:right;$|"
  r"^background-color:white;$|"
  r"^-webkit-text-stroke-width:0px;$|"
  r"^font-size:17\.6px;$|"
  r"^font-variant-caps:normal;$|"
  r"^font-variant-ligatures:normal;$|"
  r"^font-weight:400;$|"
  r"^letter-spacing:normal;$|"
  r"^orphans:|"
  r"^text-align:start;$|"
  r"^text-decoration-.+:initial;$|"
  r"^text-indent:0px;$|"
  r"^text-transform:none;$|"
  r"^white-space:normal;$|"
  r"^widows:|"
  r"^word-spacing:0px;$"
)

def clean_attrs(attrs: dict[str, str]) -> dict[str, str]:
  return {key: value for key, value in attrs.items() if not ATTR_BLACKLIST.search(key)}

def clean_css(string: str) -> list[str]:
  styles = [style.replace(" ", "") + ";" for style in string.strip(";").split(";")]
  return [style for style in styles if not CSS_BLACKLIST.search(style)]