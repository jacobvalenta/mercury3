from decimal import Decimal

from django import forms

from mercury3.customers.models import Customer
from mercury3.items.models import Item

from .models import Transaction, TransactionItem


class TransactionForm(forms.ModelForm):
	# customer = forms.ModelChoiceField(queryset=Customer.objects.all())

	class Meta:
		model = Transaction
		fields = ["customer", "transaction_type"]

	def save(self, item_data, commit=True, *args, **kwargs):
		transaction = super().save(commit=False, *args, **kwargs)

		subtotal = sum([item['price'] for item in item_data])

		if transaction.transaction_type in [Transaction.SALE, Transaction.LAYAWAY]:
			tax = subtotal * Decimal(0.06)
		else:
			tax = Decimal(0.00)

		total = subtotal + tax

		transaction.subtotal = subtotal
		transaction.tax = tax
		transaction.total = total

		if commit:
			transaction.save()

			for item in item_data:
				titem = TransactionItem(transaction=transaction,
										item=item['item'],
										price=item['price'])
				titem.save()

			return transaction
		else:
			raise Warning("TransactionForm.save(commit=False) does not save items.")
			return transaction


class TransactionItemForm(forms.Form):
	item = forms.ModelChoiceField(queryset=Item.objects.all())
	price = forms.DecimalField(max_digits=9, decimal_places=2)