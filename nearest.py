import hookline
import argparse
from datetime import date

def next_schedule_date(datefloor, schedule):
	next_date = next(filter(lambda x: x > datefloor, sorted(schedule.keys())), None)
	if next_date is None:
		raise Exception('No schedule dates after %s' % datefloor.isoformat())
	return next_date

def print_schedule_time_r(time, schedule_time):
	print('\t' + time.strftime('%I:%M %p').lower())
	rev_a = {}
	for assignment in schedule_time.keys():
		for person in hookline.flatten_list(schedule_time[assignment]):
			if person not in rev_a:
				rev_a[person] = []
			rev_a[person].append(assignment)
	for person in sorted(rev_a.keys()):
		print('\t\t%s: %s' % (person, ', '.join(rev_a[person])))

def print_schedule_date_r(day, schedule_date):
	print(day.strftime('%A, %B %m, %Y'))
	for t in sorted(schedule_date.keys()):
		print_schedule_time_r(t, schedule_date[t])

parser = argparse.ArgumentParser(description='Print the schedule for the next event')
parser.add_argument('-r', '--reverse', dest='reverse', action='store_true',
					help='show schedule by person rather than assignment')
args = parser.parse_args()

schedule = hookline.get_schedule(hookline.feed_url)
day = next_schedule_date(date.today(), schedule)

if args.reverse:
	print_schedule_date_r(day, schedule[day])
else:
	hookline.dump_schedule_date(day, schedule[day])
