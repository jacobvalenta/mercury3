from django.db import models

class Store(models.Model):
	name = models.CharField(max_length=32)

	balance = models.DecimalField(max_digits=9, decimal_places=2)

	def __str__(self):
		return self.name

class Location(models.Model):
	store = models.ForeignKey('Store', on_delete=models.CASCADE)
	name = models.CharField(max_length=8)

	def __str__(self):
		return self.name