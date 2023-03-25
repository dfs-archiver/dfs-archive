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
  r"^data-blogger-escaped-|"
  r"^data-(?:dobid|decimal|entity|id|event-action)$|"
  r"data-v-|"
  r"^action$|"
  r"^tabindex$|"
  r"^method$|"
  r"^type$"
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
  r"^float:|"
  r"^background-color:white;$|"
  r"^-webkit-text-stroke-width:0px;$|" 
  r"^font-size:|"
  r"^font-variant-caps:normal;$|"
  r"^font-variant-ligatures:normal;$|"
  r"^font-weight:|"
  r"^letter-spacing:normal;$|"
  r"^orphans:|"
  r"^text-align:(?:start|left);$|"
  r"^text-decoration-.+:initial;$|"
  r"^text-indent:0px;$|"
  r"^text-transform:none;$|"
  r"^white-space:normal;$|"
  r"^widows:|"
  r"^word-spacing:0px;$|"
  r"^text-decoration:underline;$|"
  r"^display:inline;$|"
  r"^font-family:(?:ciscosansttregular|Arial);|"
  r"^border|"
  r"^position:relative;$"
)

def clean_attrs(attrs: dict[str, str]) -> dict[str, str]:
  return {key: value for key, value in attrs.items() if not ATTR_BLACKLIST.search(key)}

def clean_css(string: str) -> list[str]:
  styles = [style.replace(" ", "") + ";" for style in string.strip(";").split(";")]
  return [style for style in styles if not CSS_BLACKLIST.search(style)]