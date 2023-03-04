from django.db import models

from mercury3.utils import STATE_CHOICES

class Customer(models.Model):
	first_name = models.CharField(max_length=24)
	middle_name = models.CharField(max_length=24, blank=True, null=True)
	last_name = models.CharField(max_length=24)

	address_1 = models.CharField(max_length=48)
	address_2 = models.CharField(max_length=48, blank=True, null=True)

	city = models.CharField(max_length=32)
	state = models.CharField(max_length=2, choices=STATE_CHOICES)
	zip_code = models.CharField(max_length=5)

	phone_number = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return ' '.join(filter(None, (self.first_name, self.middle_name, self.last_name)))