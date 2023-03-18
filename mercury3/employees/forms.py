import re

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

from mercury3.stores.models import Store
from mercury3.utils import get_trailing_number

from .models import Employee

class UserForm(forms.Form):
	first_name = forms.CharField(max_length=24)
	last_name = forms.CharField(max_length=24)

	password1 = forms.CharField(widget=PasswordInput, label="Password")
	password2 = forms.CharField(widget=PasswordInput, label="Repeat Password")

	def is_valid(self, *args, **kwargs):
		valid = super().is_valid(*args, **kwargs)
		
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			valid = False

		return valid

	def generate_username(self):
		username_base = "{0}{1}".format(self.cleaned_data['first_name'][0],
										self.cleaned_data['last_name'])
		username_base = username_base.lower()

		similar_usernames = User.objects.filter( \
			username__startswith=username_base)

		number = 0
		highest_increment = 0

		for user in similar_usernames:
			number = get_trailing_number(user.username)

			if not number:
				number = 0

			if number > highest_increment:
				highest_increment = number

		if number > 0:
			suffix = number
		else:
			suffix = ""

		username = "{}{}".format(username_base, suffix)

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