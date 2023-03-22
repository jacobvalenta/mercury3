from django import forms

from .models import Drawer

class OpenDrawerForm(forms.ModelForm):
	class Meta:
		model = Drawer
		fields = ["balance",]

	def save(self, commit=True):
		if commit:
			self.instance.save()

		return self.instance

class CloseDrawerForm(forms.ModelForm):
	class Meta:
		model = Drawer
		fields = ["balance",]

	def save(self, commit=True):
		if commit:
			self.instance.close()

		return self.instance

