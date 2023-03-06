from django.db import models

class Item(models.Model):
	STATUS_CHOICES = (
		('sale', "Sellable"),
		('hold', "Hold")
	)

	make = models.CharField(max_length=48, blank=True, null=True)
	model = models.CharField(max_length=48, blank=True, null=True)

	price_in = models.DecimalField(max_digits=9, decimal_places=2)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	price_out = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

	status = models.CharField(max_length=10, choices=STATUS_CHOICES)

	def __str__(self):
		return "{0} {1}".format(self.make if self.make else '', self.model).strip()