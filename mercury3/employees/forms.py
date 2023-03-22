import re

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

from mercury3.stores.models import Store
from mercury3.utils import get_trailing_number, generate_username

from .models import Employee

class UserForm(forms.ModelForm):
	password1 = forms.CharField(widget=PasswordInput, label="Password",
								required=False)
	password2 = forms.CharField(widget=PasswordInput, label="Repeat Password",
								required=False)

	class Meta:
		model = User
		fields = ["password1", "password2"]

	def is_valid(self, *args, **kwargs):
		valid = super().is_valid(*args, **kwargs)
		
		# If passwords do not match: fail
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			valid = False

		# If password is not set on new user: fail
		if not self.instance.pk and self.cleaned_data['password1'] == "":
			valid = False

		return valid

	def save(self, first_name, last_name, commit=True):
		if self.instance.pk:
			user = self.instance

			if self.cleaned_data['password1']:
				user.set_password(self.cleaned_data['password1'])
				user.save()
		else:
			user = User.objects.create_user(\
				generate_username(first_name, last_name),
				password=self.cleaned_data['password1'])

		return user

class EmployeeForm(forms.ModelForm):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)

	store = forms.ModelChoiceField(queryset=Store.objects.all())

	class Meta:
		model = Employee
		fields = ["first_name", "last_name", "store"]

	def save(self, user, commit=True):
		if self.instance.pk:
			employee = self.instance
			employee.store = self.cleaned_data['store']
			employee.first_name = self.cleaned_data['first_name']
			employee.last_name = self.cleaned_data['last_name']
		else:
			employee = Employee(user=user, store=self.cleaned_data['store'],
								first_name=self.cleaned_data['first_name'],
								last_name=self.cleaned_data['last_name'])
		if commit:
			employee.save()
		return employee