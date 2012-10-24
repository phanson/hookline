import re
import feedparser
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

# Location of schedule ATOM feed
feed_url = "http://ministryschedule.actsii.org/feeds/posts/default"

def clean(string):
    """ Removes known unwanted characters from strings in the feed. """
    return string.replace('\xa0','')

def fix_headers(soup):
    """ Adds a break tag after every header that is missing one. """
    b = soup.findAll('strong')
    for h in b:
        if re.search('\d+', str(h.string)):
            if not isinstance(h.nextSibling, Tag) or h.nextSibling.name != 'br':
                h.insert_after(Tag(name='br'))

def fix_sameline(soup, assignments):
    """ Moves the given assignments to their own line when they are
        found one the same line as another assignment. """
    for m in assignments:
        for child in soup.children:
            if isinstance(child, NavigableString):
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

def fix_extras(soup, extras):
    """ Removes unwanted assignments. """
    for child in soup.children:
        if isinstance(child, NavigableString):
            for x in extras:
                if child.string.strip().lower().startswith(x.strip().lower()):
                    child.extract()

def get_lines(soup):
    """ Returns the text of each break-separated line in the document,
        stripping away all HTML tags. """
    lines = ['']
    for child in soup.children:
        if isinstance(child, Tag) and child.name == 'br':
            lines.append('')
        else:
            if child.string is not None:
                lines[-1] += clean(child.string)
    return [line.strip() for line in lines]

def parse_schedule(lines):
    """ Parses a feed from read_feed and returns a dictionary of assignments by date. """
    pass

def read_feed(url):
    """ Pulls the feed down and puts it into a list of strings. """
    feed = feedparser.parse(feed_url)
    lines = []
    for item in feed['items']:
        for contentPart in item['content']:
            soup = BeautifulSoup(contentPart['value'])
            fix_headers(soup)
            fix_sameline(soup, ['Bass','Churchview','Sound Board'])
            fix_extras(soup, ['Sound Booth'])
            for line in get_lines(soup):
                if len(line.strip()) > 0:
                    lines.append(line)
    return lines

def get_schedule(url):
    """ Gets the given schedule and returns a dictionary of assignments by date. """
    return parse_schedule(read_feed(url))
