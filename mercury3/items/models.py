from django.apps import apps
from django.db import models
from django.db.models import Q

class Item(models.Model):
	PAWN = "pawn"
	REDEEMED = "redeem"
	SALEABLE = "saleable"
	SOLD = "sold"
	HOLD = "hold"
	POLICE_HOLD = "police_hold"
	MISSING = "missing"

	STATUS_CHOICES = (
		(PAWN, "Pawn"),
		(REDEEMED, "Redeemed"),
		(SALEABLE, "Saleable"),
		(SOLD, "Sold"),
		(HOLD, "Hold"),
		(POLICE_HOLD, "Police Hold"),
		(MISSING, "Missing")
	)

	make = models.CharField(max_length=48, blank=True, null=True)
	model = models.CharField(max_length=48, blank=True, null=True)

	price_in = models.DecimalField(max_digits=9, decimal_places=2)
	price = models.DecimalField(max_digits=9, decimal_places=2,
								blank=True, null=True)
	price_out = models.DecimalField(max_digits=9, decimal_places=2,
									blank=True, null=True)

	status = models.CharField(max_length=11, choices=STATUS_CHOICES)

	location = models.ForeignKey('stores.Location', blank=True, null=True,
								 on_delete=models.SET_NULL)

	def __str__(self):
		desc = "{0} {1}".format(self.make if self.make else '',
							    self.model if self.model else '').strip()
		return desc

	def get_absolute_url(self):
		return "/items/{0}/".format(self.pk)

	def relocate(self, user, location):
		Log = apps.get_model('logs.Log')

		self.location = location
		self.save()

		msg_template = "moved item ({}) to {}"
		msg = msg_template.format(str(self), self.location.name)
		Log.objects.create(user=user, message=msg)


class InventoryAudit(models.Model):
	time_start = models.DateTimeField(auto_now_add=True)
	time_end = models.DateTimeField(blank=True, null=True)

	items = models.ManyToManyField('Item', related_name="all_inventory",
								   blank=True)
	items_left = models.ManyToManyField('Item', related_name="inventory_left",
										blank=True)

	def save(self, *args, **kwargs):
		add_items = False
		if not self.pk:
			add_items = True

		super().save(*args, **kwargs)

		if add_items:
			items = Item.objects.all().exclude(Q(status=Item.REDEEMED) | \
											   Q(status=Item.SOLD))
			self.items.add(*items)
			self.items_left.add(*items)

	@property
	def duration(self):
		return self.time_end - self.time_start

	@property
	def scanned_items_count(self):
		return self.items.count() - self.items_left.count()
	