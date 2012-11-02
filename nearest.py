import hookline
from datetime import date

def next_schedule_date(datefloor, schedule):
    for key in sorted(schedule.keys()):
        if key >= datefloor:
            return key
    raise Exception('No schedule dates after %s' % datefloor.isoformat())

schedule = hookline.get_schedule(hookline.feed_url)
day = next_schedule_date(date.today(), schedule)

hookline.dump_schedule_date(day, schedule[day])
