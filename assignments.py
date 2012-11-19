import sys
import hookline
from datetime import datetime

def dump_assignment(assignment):
	ts = assignment[0]
	people = assignment[1]
	print('%s, %s: %s' % (ts.date().strftime('%A, %B %d'), ts.time().strftime('%I:%M %p').lower(), people))

def dump_assignments(assignments):
	for n in assignments:
		dump_assignment(n)

if len(sys.argv) > 1:
	name = sys.argv[1]
	s = hookline.get_schedule(hookline.feed_url)
	a = hookline.extract_assignments(s, name)
	dump_assignments([n for n in a if n[0] >= datetime.now()])
else:
	print('usage: %s <name>' % sys.argv[0])
