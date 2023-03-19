from decimal import Decimal

from django import forms

from mercury3.customers.models import Customer
from mercury3.items.models import Item
from mercury3.pawn_loans.models import PawnLoan

from .models import Transaction, TransactionItem


class TransactionForm(forms.ModelForm):
	# customer = forms.ModelChoiceField(queryset=Customer.objects.all())

	class Meta:
		model = Transaction
		fields = ["customer", "transaction_type"]

	def save(self, item_data, user, commit=True, *args, **kwargs):
		transaction = super().save(commit=False, *args, **kwargs)

		transaction.employee = user.employee

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


			if transaction.transaction_type == Transaction.PAWN:
				pawn_loan = transaction.pawnloan_set.first()
				for item in transaction.items.all():
					pawn_loan.items.add(item)

			return transaction
		else:
			raise Warning("TransactionForm.save(commit=False) does not save items.")
			return transaction


class TransactionItemForm(forms.Form):
	item = forms.ModelChoiceField(queryset=Item.objects.all())
	price = forms.DecimalField(max_digits=9, decimal_places=2)


class PayOrRedeemPawnForm(forms.Form):
	PAY_OR_REDEEM_CHOICES = (
		(Transaction.PAYMENT, "Pay"),
		(Transaction.REDEEM, "Redeem")
	)

	customer = forms.ModelChoiceField(queryset=Customer.objects.all())
	pawn_loan = forms.ModelChoiceField(queryset=PawnLoan.objects.active())

	transaction_type = forms.ChoiceField(choices=PAY_OR_REDEEM_CHOICES)

	payment_amount = forms.DecimalField(max_digits=9, decimal_places=2)

	def save(self, user, *args, **kwargs):
		transaction_type = self.cleaned_data['transaction_type']
		customer = self.cleaned_data['customer']
		subtotal = self.cleaned_data['payment_amount']
		tax = subtotal * Decimal(0.06)
		total = subtotal + tax

		pawn_loan = self.cleaned_data['pawn_loan']

		transaction = Transaction(transaction_type=transaction_type,
								  customer=customer,
								  subtotal=subtotal,
								  tax=tax,
								  total=total,
								  employee=user.employee)
		transaction.save(pawn_loan=pawn_loan)

		return transaction