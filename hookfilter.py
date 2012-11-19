import hookline

def day_by_assignment(assignments, inverted, schedule_day):
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

def by_assignment(assignments, inverted, schedule):
	filtered_schedule = {}
	for day, schedule_day in schedule.items():
		filtered_schedule[day] = day_by_assignment(assignments, inverted, schedule_day)
	return filtered_schedule

def day_by_name(names, inverted, schedule_day):
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

def by_name(names, inverted, schedule):
	filtered_schedule = {}
	for day, schedule_day in schedule.items():
		filtered_schedule[day] = day_by_name(names, inverted, schedule_day)
	return filtered_schedule

def has_assignments(event_tuple):
	schedule_event = event_tuple[1]
	if len(schedule_event) == 0:
		return False
	if next(filter(lambda x: len(x) > 0, schedule_event.values()), None):
		return True
	return False

def has_names(assignment_tuple):
	return len(hookline.flatten_list(assignment_tuple[1])) > 0

def clean_day(schedule_day):
	cleaned_schedule_day = {}
	for event, schedule_event in schedule_day.items():
		cleaned_schedule_day[event] = {}
		for assignment, assignees in filter(has_names, schedule_event.items()):
			cleaned_schedule_day[event][assignment] = assignees
	return dict(filter(has_assignments, cleaned_schedule_day.items()))

def has_events(day_tuple):
	return len(day_tuple[1]) > 0

def clean(schedule):
	cleaned_schedule = {}
	for day, schedule_day in schedule.items():
		cleaned_schedule[day] = clean_day(schedule_day)
	return dict(filter(has_events, cleaned_schedule.items()))
