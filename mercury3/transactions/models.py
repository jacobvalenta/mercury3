from django.db import models

class TransactionItem(models.Model):
	transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE)
	item = models.ForeignKey('items.Item', on_delete=models.CASCADE)

	price = models.DecimalField(max_digits=9, decimal_places=2)

class Transaction(models.Model):
	BUY = "buy"
	PAWN = "pawn"
	SALE = "sale"
	LAYAWAY = "layaway"

	TRANSACTION_TYPE_CHOICES = (
		(BUY, "Buy"),
		(PAWN, "Pawn"),
		(SALE, "Sale"),
		(LAYAWAY, "Layaway")
	)

	transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

	customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, blank=True, null=True)
	items = models.ManyToManyField('items.Item', through="transactions.TransactionItem")

	subtotal = models.DecimalField(max_digits=9, decimal_places=2)
	tax = models.DecimalField(max_digits=9, decimal_places=2)
	total = models.DecimalField(max_digits=9, decimal_places=2)

	timestamp = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return "/transactions/{0}/".format(self.pk)