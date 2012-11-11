import re
import feedparser
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from datetime import date, time, datetime

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

def fix_orphans(soup):
    """ Removes break tags that separate orphaned lines from their parents """
    for br in soup.findAll('br'):
        s = br.nextSibling.string
        if s and len(s) > 0 and not (re.search('\d+', s) or re.search(':', s)):
            br.extract()

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

def is_header(line):
    """ Returns True iff the given line is a header. """
    return re.search('\d+', line) is not None

def get_header_date(header):
    """ Returns the date contained in the given header. """
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    s = re.search('(%s)\s*(\d+)' % '|'.join(months), header, re.IGNORECASE)
    if not s:
        raise Exception('Could not find header month: %s' % header)
    current_year = date.today().year
    day = int(s.groups()[1])
    month = months.index(s.groups()[0]) + 1
    year = current_year if date.today().month <= month else current_year + 1
    return date(year, month, day)

def get_header_time(header):
    """ Returns the time corresponding to the given header. """
    s = re.search('(\d+)(:\d+)?\s*(am|pm)', header, re.IGNORECASE)
    if s:
        hour = int(s.groups()[0])
        minute = 0
        if s.groups()[1]:
            minute = int(s.groups()[1][1:])
        if s.groups()[2].lower() == 'pm':
            hour += 12
        return time(hour,minute)
    elif re.search('morning', header, re.IGNORECASE):
        return time(10,0)
    elif re.search('evening', header, re.IGNORECASE):
        return time(18,30)
    else:
        raise Exception('Could not find header time: %s' % header)

def parse_assignment(line):
    """ Returns an assignment:assignee tuple. """
    s = line.split(':')
    p = [a.strip() for a in s[1].split(';')]
    if len(p) == 1:
        v = [a.strip() for a in p[0].split(',')]
    else:
        v = [[a.strip() for a in i.split(',')] for i in p]
    return (s[0].strip(), v)

def parse_schedule(lines):
    """ Parses a feed from read_feed and returns a dictionary of assignments by date. """
    schedule = {}
    current_date = None
    current_time = None
    for line in lines:
        if is_header(line):
            current_date = get_header_date(line)
            if not current_date in schedule:
                schedule[current_date] = {}
            current_time = get_header_time(line)
            if not current_time in schedule[current_date]:
                schedule[current_date][current_time] = {}
        else:
            n,p = parse_assignment(line)
            schedule[current_date][current_time][n] = p
    return schedule

def flatten(soup, elements):
    for name in elements:
        for e in soup.findAll(name):
            e.replaceWithChildren()

def read_feed(url):
    """ Pulls the feed down and puts it into a sanitized list of strings. """
    feed = feedparser.parse(feed_url)
    lines = []
    for item in feed['items']:
        for contentPart in item['content']:
            soup = BeautifulSoup(contentPart['value'])
            fix_headers(soup)
            fix_sameline(soup, ['Bass','Churchview','Sound Board','Clean'])
            fix_extras(soup, ['Sound Booth'])
            flatten(soup, ['strong','b','div'])
            fix_orphans(soup)
            for line in get_lines(soup):
                if len(line.strip()) > 0:
                    lines.append(line)
    return lines

def get_schedule(url):
    """ Gets the given schedule and returns a dictionary of assignments by date. """
    return parse_schedule(read_feed(url))

def dump_schedule_assignment(assignment, people, indent_level):
    print(('\t' * indent_level) + '%s: %s' % (assignment, repr(people)))

def dump_schedule_time(time, schedule_time, indent_level = 0):
    print(('\t' * indent_level) + time.strftime('%I:%M %p').lower())
    for a in sorted(schedule_time.keys()):
        dump_schedule_assignment(a, schedule_time[a], indent_level + 1)

def dump_schedule_date(day, schedule_date, indent_level = 0):
    print(('\t' * indent_level) + day.strftime('%A, %B %m, %Y'))
    for t in sorted(schedule_date.keys()):
        dump_schedule_time(t, schedule_date[t], indent_level + 1)

def dump_schedule(schedule, indent_level = 0):
    for d in sorted(schedule.keys()):
        dump_schedule_date(d, schedule[d], indent_level + 1)

def flatten_list(scruffy_list):
    norm = [([a] if isinstance(a,str) else a) for a in scruffy_list] # normalize
    return [item for sublist in norm for item in sublist] # flatten

def extract_assignments(schedule, person):
    """ Returns a list of all the assignments for the given person. """
    assignments = []
    for edate in schedule.keys():
        for etime in schedule[edate].keys():
            for assignment in schedule[edate][etime].keys():
                for assignee in flatten_list(schedule[edate][etime][assignment]):
                    if assignee.strip().lower() == person.strip().lower():
                        ts = datetime(edate.year, edate.month, edate.day, etime.hour, etime.minute)
                        assignments.append((ts,assignment))
    return sorted(assignments, key=lambda y: y[0])

def dump_assignment(assignment):
    ts = assignment[0]
    people = assignment[1]
    print(ts.strftime('%A, %B %d, %I:%M %p') + ' ' + people)

def dump_assignments(assignments):
    for n in assignments:
        dump_assignment(n)

