import re

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

from mercury3.stores.models import Store
from mercury3.utils import get_trailing_number

from .models import Employee

class EmployeeFormsMixin(object):
	def __init__(self, *args, instance=None, **kwargs):
		self.instance = instance

		super().__init__(*args, **kwargs)

class UserForm(EmployeeFormsMixin, forms.Form):
	password1 = forms.CharField(widget=PasswordInput, label="Password",
								required=False)
	password2 = forms.CharField(widget=PasswordInput, label="Repeat Password",
								required=False)

	def is_valid(self, *args, **kwargs):
		valid = super().is_valid(*args, **kwargs)
		
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			valid = False

		if self.instance == None and self.cleaned_data['password1'] == "":
			valid = False

		return valid

	def generate_username(self, first_name, last_name):
		username_base = "{0}{1}".format(first_name[0],
										last_name)
		username_base = username_base.lower()

		similar_usernames = User.objects.filter( \
			username__startswith=username_base)

		number = -1
		highest_increment = -1

		for user in similar_usernames:
			number = get_trailing_number(user.username)

			if not number:
				number = 0

			if number > highest_increment:
				highest_increment = number

			if username_base == user.username:
				number += 0

		if number > -1:
			suffix = number +1
		else:
			suffix = ""

		username = "{}{}".format(username_base, suffix)

		return username

	def save(self, *args, first_name=None, last_name=None, **kwargs):
		if self.instance:
			user = self.instance
		else:
			user = User.objects.create_user(\
				self.generate_username(first_name, last_name),
				password=self.cleaned_data['password1'])

		user.save()

		return user

class EmployeeForm(EmployeeFormsMixin, forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)

	store = forms.ModelChoiceField(queryset=Store.objects.all())

	def save(self, user, *args, commit=True, **kwargs):
		if self.instance:
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