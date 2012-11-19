import hookline
import argparse
from datetime import date

def next_schedule_date(datefloor, schedule):
	next_date = next(filter(lambda x: x >= datefloor, sorted(schedule)), None)
	if next_date is None:
		raise Exception('No schedule dates after %s' % datefloor.isoformat())
	return next_date

def print_schedule_time_r(t, schedule_time):
	print('\t' + t.strftime('%%d:%M %p').lower() % (t.hour % 12))
	rev_a = {}
	for assignment in schedule_time:
		for person in hookline.flatten_list(schedule_time[assignment]):
			if person not in rev_a:
				rev_a[person] = []
			rev_a[person].append(assignment)
	for person in sorted(rev_a):
		print('\t\t%s: %s' % (person, ', '.join(rev_a[person])))

def print_schedule_date_r(day, schedule_date):
	print(day.strftime('%A, %B %%d, %Y') % day.day)
	for t in sorted(schedule_date.keys()):
		print_schedule_time_r(t, schedule_date[t])

def filter_assignments(assignments, inverted, schedule_day):
	if len(assignments) == 0:
		return schedule_day
	assignments = list(map(str.lower, assignments))
	filtered_schedule_day = {}
	for event in schedule_day:
		filtered_schedule_day[event] = {}
		for assignment in schedule_day[event]:
			if (assignment.lower() in assignments) ^ inverted:
				filtered_schedule_day[event][assignment] = schedule_day[event][assignment]
	return filtered_schedule_day

def filter_names(names, inverted, schedule_day):
	if len(names) == 0:
		return schedule_day
	names = list(map(str.lower, names))
	filtered_schedule_day = {}
	for event in schedule_day:
		filtered_schedule_day[event] = {}
		for assignment, assignees in schedule_day[event].items():
			if isinstance(assignees[0], list):
				filtered_schedule_day[event][assignment] = [[n for n in a if (n.lower() in names) ^ inverted] for a in assignees]
			else:
				filtered_schedule_day[event][assignment] = [n for n in assignees if (n.lower() in names) ^ inverted]
	return filtered_schedule_day

def has_assignments(event_tuple):
	schedule_event = event_tuple[1]
	if len(schedule_event) == 0:
		return False
	if next(filter(lambda x: len(x) > 0, schedule_event.values()), None):
		return True
	return False

def has_names(assignment_tuple):
	return len(hookline.flatten_list(assignment_tuple[1])) > 0

def clean(schedule_day):
	cleaned_schedule = {}
	for event, schedule_event in filter(has_assignments, schedule_day.items()):
		cleaned_schedule[event] = {}
		for assignment, assignees in filter(has_names, schedule_event.items()):
			cleaned_schedule[event][assignment] = assignees
	return cleaned_schedule

parser = argparse.ArgumentParser(description='Print the schedule for the next event.')
parser.add_argument('-r', '--reverse', dest='reverse', action='store_true',
                    help='show schedule by person rather than assignment')
parser.add_argument('-a', '--assignments', metavar='<assignment>', type=str,
                    nargs='+', dest='assignments', action='store',
                    help='list of assignments to filter by')
parser.add_argument('-n', '--names', metavar='<name>', type=str, nargs='+',
                    dest='names', action='store',
                    help='list of names to filter by')
parser.add_argument('-i', '--invert-filters', dest='invert_filters', action='store_true',
                    help='use filters as blacklists instead of whitelists')
args = parser.parse_args()

schedule = hookline.get_schedule(hookline.feed_url)
day = next_schedule_date(date.today(), schedule)
schedule_day = schedule[day]

if args.assignments:
	schedule_day = filter_assignments(args.assignments, args.invert_filters, schedule_day)
if args.names:
	schedule_day = filter_names(args.names, args.invert_filters, schedule_day)
schedule_day = clean(schedule_day)

if args.reverse:
	print_schedule_date_r(day, schedule_day)
else:
	hookline.dump_schedule_date(day, schedule_day)
