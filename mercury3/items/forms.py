from django import forms

from .models import Item

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ["make", "model", "price_in"]

class ItemScanForm(forms.Form):
	item = forms.ModelChoiceField(queryset=Item.objects.all())

	def __init__(self, *args, **kwargs):
		audit = kwargs.pop('audit', None)

		if not audit:
			raise ValueError("Audit must be set when using ItemScanForm")

		super().__init__(*args, **kwargs)

		self.fields['item'].queryset = audit.items_left.all()
