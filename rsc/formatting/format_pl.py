import re, bs4

# There's one post that has a date in the format "November, 1994"
DATE = re.compile(r"(?:\d\d?|November), 199\d$")

def format_pl(soup: bs4.BeautifulSoup, body: bs4.element.Tag) -> bs4.BeautifulSoup:
  date_header = soup.new_tag("h4")
  date_p = get_date_p(body)
  for p in date_p:
    date_header.append(p)
    if type(p) == bs4.element.Tag:
      p.unwrap()
  
  header = body.find("h3")
  if not header:
    raise Exception("Could not find header in post", soup)
  header.insert_after(date_header)
  return soup

def get_date_p(body: bs4.element.Tag) -> bs4.element.Tag:
  date_p = None
  paragraphs = list(body.find_all("p"))
  for i in range(len(paragraphs)):
    p = paragraphs[i]
    if DATE.search(p.get_text()):
      date_p = [p.extract()]
      break
  if not date_p:
    raise Exception("Could not find date in post", body)

  # there may be additional paragraphs that should be extracted
  paragraphs = list(body.find_all("p"))
  for i in range(i-1, 0, -1):
    if not is_date_p(paragraphs[i]):
      break
    date_p.insert(0, " ")
    date_p.insert(0, paragraphs[i].extract())
    print("Found additional date paragraph", str(paragraphs[i]))

  return date_p

def is_date_p(tag: bs4.element.Tag) -> bs4.element.Tag:
  if re.compile("From Pathetic Life").match(tag.get_text()):
    return False

  if DATE.search(tag.get_text()):
    return True
  if "style" in tag.attrs and tag["style"] == "text-align:center;" and len(tag.get_text()) < 50:
    return True
  else:
    return False