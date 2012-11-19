import hookline
from datetime import date, time

def get_date(day):
	return day.strftime('%A, %B %%d, %Y') % day.day

def get_people(people):
	if len(people) == 0:
		return '';
	if isinstance(people[0], list):
		return '; '.join(', '.join(sublist) for sublist in people)
	return ', '.join(people)

def assignment(assignment, people, indent_level):
	print(('\t' * indent_level) + '%s: %s' % (assignment, get_people(people)))

def event(event_time, event_schedule, indent_level = 0):
	print(('\t' * indent_level) + event_time.strftime('%%d:%M %p').lower() % (event_time.hour % 12))
	for a in sorted(event_schedule.keys()):
		assignment(a, event_schedule[a], indent_level + 1)

def day(d, day_schedule, indent_level = 0):
	print(('\t' * indent_level) + get_date(d))
	for event_time in sorted(day_schedule.keys()):
		event(event_time, day_schedule[event_time], indent_level + 1)

def schedule(schedule, indent_level = 0):
	for d in sorted(schedule.keys()):
		day(d, schedule[d], indent_level)

def event_reverse(event_time, event_schedule, indent_level = 0):
	print(('\t' * indent_level) + event_time.strftime('%%d:%M %p').lower() % (event_time.hour % 12))
	rev_a = {}
	for assignment in event_schedule:
		for person in hookline.flatten_list(event_schedule[assignment]):
			if person not in rev_a:
				rev_a[person] = []
			rev_a[person].append(assignment)
	for person in sorted(rev_a):
		print('\t\t%s: %s' % (person, ', '.join(rev_a[person])))

def day_reverse(d, day_schedule, indent_level = 0):
	print(('\t' * indent_level) + get_date(d))
	for event_time in sorted(day_schedule.keys()):
		event_reverse(event_time, day_schedule[event_time], indent_level + 1)

def schedule_reverse(schedule, indent_level = 0):
	for d in sorted(schedule.keys()):
		day_reverse(d, schedule[d], indent_level)
