import hookline
import hookout as output
import argparse

parser = argparse.ArgumentParser(description='Print the entire schedule.')
parser.add_argument('-r', '--reverse', dest='reverse', action='store_true',
                    help='show schedule by person rather than assignment')
args = parser.parse_args()

schedule = hookline.get_schedule(hookline.feed_url)
if args.reverse:
	output.schedule_reverse(schedule)
else:
	output.schedule(schedule)
