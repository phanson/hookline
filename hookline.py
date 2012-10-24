import feedparser
from bs4 import BeautifulSoup

# via http://stackoverflow.com/questions/3593784/html-to-text-conversion-using-python-language
def gettextonly(soup):
    v=soup.string
    if v == None:
        c=soup.contents
        resulttext=''
        for t in c:
            subtext=gettextonly(t)
            resulttext+=subtext+'\n'
        return resulttext
    else:
        return v.strip()


feed_url = "http://ministryschedule.actsii.org/feeds/posts/default"
feed = feedparser.parse(feed_url)

for item in feed['items']:
    for contentPart in item['content']:
        soup = BeautifulSoup(contentPart['value'])
        s = gettextonly(soup).strip()
        lines = s.split('\n\n')
        for line in lines:
            print(line)
