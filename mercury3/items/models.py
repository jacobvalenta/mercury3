from django.db import models

class Item(models.Model):
	PAWN = "pawn"
	REDEEMED = "redeem"
	SALEABLE = "saleable"
	SOLD = "sold"
	HOLD = "hold"
	POLICE_HOLD = "police_hold"

	STATUS_CHOICES = (
		(PAWN, "Pawn"),
		(REDEEMED, "Redeemed"),
		(SALEABLE, "Saleable"),
		(SOLD, "Sold"),
		(HOLD, "Hold"),
		(POLICE_HOLD, "Police Hold")
	)

	make = models.CharField(max_length=48, blank=True, null=True)
	model = models.CharField(max_length=48, blank=True, null=True)

	price_in = models.DecimalField(max_digits=9, decimal_places=2)
	price = models.DecimalField(max_digits=9, decimal_places=2,
								blank=True, null=True)
	price_out = models.DecimalField(max_digits=9, decimal_places=2,
									blank=True, null=True)

	status = models.CharField(max_length=11, choices=STATUS_CHOICES)

	def __str__(self):
		desc = "{0} {1}".format(self.make if self.make else '',
							    self.model if self.model else '').strip()
		return desc

	def get_absolute_url(self):
		return "/items/{0}/".format(self.pk)