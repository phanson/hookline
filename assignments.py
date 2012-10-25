import sys
import hookline
from datetime import datetime

if len(sys.argv) > 1:
    name = sys.argv[1]
    s = hookline.get_schedule(hookline.feed_url)
    a = hookline.extract_assignments(s, name)
    hookline.dump_assignments([n for n in a if n[0] >= datetime.now()])
else:
    print('usage: %s <name>' % sys.argv[0])
