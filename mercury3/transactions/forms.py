from django import forms

from mercury3.customers.models import Customer
from mercury3.items.models import Item

from .models import Transaction

class TransactionForm(forms.ModelForm):
	customer = forms.ModelChoiceField(queryset=Customer.objects.all())

	class Meta:
		model = Transaction
		fields = ["customer",]

class TransactionItemForm(forms.Form):
	item = forms.ModelChoiceField(queryset=Item.objects.all())
	price = forms.DecimalField(max_digits=9, decimal_places=2)