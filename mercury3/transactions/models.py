from datetime import timedelta
from decimal import Decimal

from django.apps import apps
from django.db import models
from django.utils import timezone

from mercury3.pawn_loans.models import PawnLoan

class Transaction(models.Model):
	BUY = "buy"
	PAWN = "pawn"
	SALE = "sale"
	LAYAWAY = "layaway"
	PAYMENT = "payment"
	REDEEM = "redeem"

	TRANSACTION_TYPE_CHOICES = (
		(BUY, "Buy"),
		(PAWN, "Pawn"),
		(SALE, "Sale"),
		(LAYAWAY, "Layaway"),
		(PAYMENT, "Payment"),
		(REDEEM, "Redeem")
	)
	"""The options for `transaction_type`"""

	transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

	customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, blank=True, null=True)
	items = models.ManyToManyField('items.Item', through="transactions.TransactionItem")

	subtotal = models.DecimalField(max_digits=9, decimal_places=2)
	tax = models.DecimalField(max_digits=9, decimal_places=2)
	total = models.DecimalField(max_digits=9, decimal_places=2)

	timestamp = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		"""A direct URL for the Transaction."""
		return "/transactions/{0}/".format(self.pk)

	def save(self, pawn_loan=None, *args, **kwargs):
		Item = apps.get_model('items.Item')

		create_pawnloan = False
		if not self.pk and self.transaction_type == self.PAWN:
			create_pawnloan = True 

		super().save(*args, **kwargs)

		if self.transaction_type in [self.PAYMENT, self.REDEEM]:
			for item in pawn_loan.items.all():
				price = (item.price_in / pawn_loan.principle_amount) * self.subtotal
				t_item = TransactionItem(item=item, transaction=self, price=price)
				t_item.save()
				# transaction.add(item)

			if pawn_loan.amount_due < self.subtotal:
				working_carry = self.subtotal - pawn_loan.amount_due
				pawn_loan.amount_due = Decimal(0.00)
				pawn_loan.unpaid_principle -= working_carry
			else:
				pawn_loan.amount_due -= self.subtotal


			if self.transaction_type == self.REDEEM:
				pawn_loan.status = PawnLoan.REDEEMED
				
				for item in pawn_loan.items.all():
					item.status = Item.REDEEMED
					item.price_out = item.price_in
					item.save()

			pawn_loan.save()

		elif create_pawnloan:
			amount_due = amount_due=self.total * Decimal(0.20)
			date_due = timezone.now().date() + timedelta(days=30)

			pawn_loan = PawnLoan(customer=self.customer,
								 status=PawnLoan.ACTIVE,
								 principle_amount=self.total,
								 unpaid_principle=self.total,
								 amount_due=amount_due,
								 date_due=date_due)
			pawn_loan.save()

			for item in self.items.all():
				pawn_loan.items.add(item)

			pawn_loan.transactions.add(self)


class TransactionItem(models.Model):
	transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE)
	item = models.ForeignKey('items.Item', on_delete=models.CASCADE)

	price = models.DecimalField(max_digits=9, decimal_places=2)