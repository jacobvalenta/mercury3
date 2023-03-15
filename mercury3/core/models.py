from django.db import models

class PlanManager(models.Manager):
    def active(self):
        return self.filter(status="active")


class Plan(models.Model):
	ACTIVE = "active"
	REDEEMED = "redeemed"
	FORFEITED = "forfeited"

	STAUS_CHOICES = (
		(ACTIVE, "Active"),
		(REDEEMED, "Redeemed"),
		(FORFEITED, "Forfeited")
	)

	customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)

	status = models.CharField(max_length=10, choices=STAUS_CHOICES)

	principle_amount = models.DecimalField(max_digits=9, decimal_places=2)
	unpaid_principle = models.DecimalField(max_digits=9, decimal_places=2)

	amount_due = models.DecimalField(max_digits=9, decimal_places=2)
	date_due = models.DateField(blank=True, null=True)

	items = models.ManyToManyField('items.Item')
	transactions = models.ManyToManyField('transactions.Transaction')

	objects = PlanManager()

	class Meta:
		abstract = True

	@property
	def items_description(self):
		if self.items.count() == 1:
			return str(self.items.all()[0])
		elif self.items.count() > 1:
			return "{0} items".format(self.items.count)