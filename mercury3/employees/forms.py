import hashlib
import uuid

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

from mercury3.stores.models import Store

from .models import Employee

class UserForm(forms.Form):
	first_name = forms.CharField(max_length=24)
	last_name = forms.CharField(max_length=24)

	password1 = forms.CharField(widget=PasswordInput)
	password2 = forms.CharField(widget=PasswordInput)

	def is_valid(self, *args, **kwargs):
		valid = super().is_valid(*args, **kwargs)
		
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			valid = False

		return valid


	def generate_username(self):
		username = hashlib.sha1( \
			"{0}_{1}_{2}".format(self.cleaned_data['first_name'],
								 self.cleaned_data['last_name'],
								 uuid.uuid4().hex) \
						 .encode('UTF-8')).hexdigest()[0:13]

		return username

	def save(self, *args, **kwargs):
		user = User.objects.create_user(\
			self.generate_username(),
			password=self.cleaned_data['password1'])

		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]

		user.save()

		return user

class EmployeeForm(forms.Form):
	store = forms.ModelChoiceField(queryset=Store.objects.all())

	def save(self, user, *args, **kwargs):
		employee = Employee(user=user, store=self.cleaned_data['store'])
		employee.save()
		return employee