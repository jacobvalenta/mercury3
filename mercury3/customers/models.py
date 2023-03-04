from django.db import models

class Customer(models.Model):
	first_name = models.CharField(max_length=24)
	middle_name = models.CharField(max_length=24, blank=True, null=True)
	last_name = models.CharField(max_length=24)
