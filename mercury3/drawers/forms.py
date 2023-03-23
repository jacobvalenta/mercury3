from django import forms

from .models import DrawerIdentifier, Drawer

class OpenDrawerForm(forms.ModelForm):
	identifier_key = forms.ModelChoiceField(
		queryset=DrawerIdentifier.objects.not_open(),
		label="Name",
		required=False)

	class Meta:
		model = Drawer
		fields = ["identifier_key", "balance",]

	def save(self, user=None, commit=True):
		if commit:
			if not user:
				raise ValueError("`user` must be set when saving.")
			self.instance.save(user=user)

		return self.instance

class CloseDrawerForm(forms.ModelForm):
	class Meta:
		model = Drawer
		fields = ["balance",]

	def save(self, user, commit=True):
		if commit:
			self.instance.close(user=user)

		return self.instance