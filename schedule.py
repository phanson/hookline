import hookline
import hookfilter as filter_schedule
import hookout as output
import argparse

parser = argparse.ArgumentParser(description='Print the entire schedule.')
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

if args.assignments:
	schedule = filter_schedule.by_assignment(args.assignments, args.invert_filters, schedule)
if args.names:
	schedule = filter_schedule.by_name(args.names, args.invert_filters, schedule)
schedule = filter_schedule.clean(schedule)

if args.reverse:
	output.schedule_reverse(schedule)
else:
	output.schedule(schedule)
