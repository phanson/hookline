import re
import feedparser
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

def clean(string):
    return string.replace('\xa0','')

def fix_headers(soup):
    """ Adds a break tag after every header that is missing one. """
    b = soup.findAll('strong')
    for h in b:
        if re.search('\d+', str(h.string)):
            if not isinstance(h.nextSibling, Tag) or h.nextSibling.name != 'br':
                h.insert_after(Tag(name='br'))

def fix_sameline(soup, assignments):
    for child in soup.children:
        if isinstance(child, NavigableString):
            for m in assignments:
                s = re.search(m+':', child.string, re.IGNORECASE)
                if s and s.start() > 0:
                    p = child.previous
                    a,b = child.string[:s.start()], child.string[s.start():]
                    child.extract()
                    # need to insert in reverse order
                    # because we are inserting after the same element
                    p.insert_after(b.strip())
                    p.insert_after(Tag(name='br'))
                    p.insert_after(a.strip())

def get_lines(soup):
    lines = ['']
    for child in soup.children:
        if isinstance(child, Tag) and child.name == 'br':
            lines.append('')
        else:
            if child.string is not None:
                lines[-1] += clean(child.string)
    return [line.strip() for line in lines]

feed_url = "http://ministryschedule.actsii.org/feeds/posts/default"
feed = feedparser.parse(feed_url)

lines = []
for item in feed['items']:
    for contentPart in item['content']:
        soup = BeautifulSoup(contentPart['value'])
        fix_headers(soup)
        fix_sameline(soup, ['Bass','Churchview','Sound Board'])
        for line in get_lines(soup):
            if len(line.strip()) > 0:
                lines.append(line)
