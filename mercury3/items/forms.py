from django import forms

from mercury3.stores.models import Location

from .models import Item, Bucket

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

class SetItemLocationForm(forms.ModelForm):
	location = forms.ModelChoiceField(queryset=Location.objects.all(),
									  required=False)

	class Meta:
		model = Item
		fields = ["location"]

	def save(self, user, commit=True, **kwargs):
		if commit:
			location = self.cleaned_data['location']
			self.instance.relocate(user=user, location=location)

		return self.instance

class MoveItemToBucketForm(forms.ModelForm):
	bucket = forms.ModelChoiceField(queryset=Bucket.objects.all())

	class Meta:
		model = Item
		fields = ["bucket"]

	def save(self, user, commit=True, **kwargs):
		if commit:
			self.instance.add_to_bucket(user=user,
			                            bucket=self.cleaned_data["bucket"])

		return self.instance