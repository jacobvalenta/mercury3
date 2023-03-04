from django.db import models

class TransactionItem(models.Model):
	transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE)
	item = models.ForeignKey('items.Item', on_delete=models.CASCADE)

	price = models.DecimalField(max_digits=9, decimal_places=2)

class Transaction(models.Model):
	customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
	items = models.ManyToManyField('items.Item', through="transactions.TransactionItem")

	sub_total = models.DecimalField(max_digits=9, decimal_places=2)
	tax = models.DecimalField(max_digits=9, decimal_places=2)
	total = models.DecimalField(max_digits=9, decimal_places=2)

	timestamp = models.DateTimeField(auto_now_add=True)