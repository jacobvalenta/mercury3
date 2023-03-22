import re

from django.apps import apps

STATE_CHOICES = (
	('AL', "Alabama"),
	('AK', "Alaska"),
	('AZ', "Arizona"),
	('AR', "Arkansas"),
	('CA', "California"),
	('CO', "Colorado"),
	('CT', "Connecticut"),
	('DE', "Delaware"),
	('FL', "Florida"),
	('GA', "Georgia"),
	('HI', "Hawaii"),
	('ID', "Idaho"),
	('IL', "Illinois"),
	('IN', "Indiana"),
	('IA', "Iowa"),
	('KS', "Kansas"),
	('KY', "Kentucky"),
	('LA', "Louisiana"),
	('ME', "Maine"),
	('MD', "Maryland"),
	('MA', "Massachusetts"),
	('MI', "Michigan"),
	('MN', "Minnesota"),
	('MS', "Mississippi"),
	('MO', "Missouri"),
	('MT', "Montana"),
	('NE', "Nebraska"),
	('NV', "Nevada"),
	('NH', "New Hampshire"),
	('NJ', "New Jersey"),
	('NM', "New Mexico"),
	('NY', "New York"),
	('NC', "North Carolina"),
	('ND', "North Dakota"),
	('OH', "Ohio"),
	('OK', "Oklahoma"),
	('OR', "Oregon"),
	('PA', "Pennsylvania"),
	('RI', "Rhode Island"),
	('SC', "South Carolina"),
	('SD', "South Dakota"),
	('TN', "Tennessee"),
	('TX', "Texas"),
	('UT', "Utah"),
	('VT', "Vermont"),
	('VA', "Virginia"),
	('WA', "Washington"),
	('WV', "West Virginia"),
	('WI', "Wisconsin"),
	('WY', "Wyoming")
)
"""A list of the 50 state choices."""

TWO_SECONDS = 2000000
"""2 Seconds expressed in microseconds."""

def get_pk_from_url(url):
	"""Get a PK from simple url."""
	try:
		return int(url.split('/')[2])
	except IndexError:
		return None
	except ValueError:
		return None

def is_number(check_value):
	try:
		int(check_value)
		return True
	except ValueError:
		return False

def get_trailing_number(s):
	"""Returns the number from the end of string.

	Thank you to efotinis from
	[StackOverflow](https://stackoverflow.com/questions/7085512/)
	"""
	m = re.search(r'\d+$', s)
	return int(m.group()) if m else None

def generate_username(first_name, last_name):
	if not first_name or not last_name:
		raise ValueError("first_name and last_name required.")

	User = apps.get_model('auth.User')

	username_base = "{0}{1}".format(first_name[0],
									last_name)
	username_base = username_base.lower()

	similar_usernames = User.objects.filter( \
		username__startswith=username_base)

	number = -1
	highest_increment = -1

	for user in similar_usernames:
		number = get_trailing_number(user.username)

		if username_base == user.username:
			number == 0
		if not number:
			number = 0
		elif number > highest_increment:
			highest_increment = number

	if number > -1:
		suffix = number +1
	else:
		suffix = ""

	username = "{}{}".format(username_base, suffix)

	return username