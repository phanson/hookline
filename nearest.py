import hookline
import hookfilter as filter_schedule
import hookout as output
import argparse
from datetime import date

def next_schedule_date(datefloor, schedule):
	next_date = next(filter(lambda x: x >= datefloor, sorted(schedule)), None)
	if next_date is None:
		raise Exception('No schedule dates after %s' % datefloor.isoformat())
	return next_date

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
	schedule_day = filter_schedule.by_assignment(args.assignments, args.invert_filters, schedule_day)
if args.names:
	schedule_day = filter_schedule.by_name(args.names, args.invert_filters, schedule_day)
schedule_day = filter_schedule.clean(schedule_day)

if args.reverse:
	output.day_reverse(day, schedule_day)
else:
	output.day(day, schedule_day)
