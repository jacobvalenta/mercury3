import re

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