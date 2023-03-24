# from decimal import Decimal

# from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone

from mercury3.utils import get_pk_from_url

from .models import Employee

class EmployeeTestCase(TestCase):
	fixtures = ["stores_test.json", "customers_test.json",
				"employees_test.json"]

	def test_employee_management_200(self):
		"""Test employee management."""
		response = self.client.get(reverse('employees:manage'))
		self.assertEqual(response.status_code, 200)

	def test_employee_list_200(self):
		"""Test employee list"""
		response = self.client.get(reverse('employees:list'))
		self.assertEqual(response.status_code, 200)

	def test_employee_create(self):
		"""Test employee create. Tests that response is a redirect
		and validates the following fields: `first_name`, `last_name`,
		and `user.username`."""

		post_data = {
			'first_name': "New", 
			'last_name': "Employee",
			'store': 1,
			'password1': 'testpassword',
			'password2': 'testpassword'
		}

		# Response is a redirect
		self.client.login(username='temployee', password='brickandmortar')
		response = self.client.post(reverse('employees:create'),
									post_data)
		self.assertEqual(response.status_code, 302)

		url = response.headers['Location']
		pk = get_pk_from_url(url)
		self.assertEqual(pk, 2)

		# Get employee and test `first_name`, `last_name` and
		# `user.username`
		employee = Employee.objects.all().order_by('-pk').first()

		self.assertEqual(employee.first_name, "New")
		self.assertEqual(employee.last_name, "Employee")
		self.assertEqual(employee.user.username, "nemployee")

	def test_employee_update(self):
		post_data = {
			'first_name': "Testing", 
			'last_name': "Employee",
			'store': 1,
			'password1': '',
			'password2': ''
		}

		# Response is a redirect
		self.client.login(username='temployee', password='brickandmortar')
		url = reverse('employees:update', kwargs={'pk': 1})
		response = self.client.post(url, post_data)
		self.assertEqual(response.status_code, 302)

		url = response.headers['Location']
		self.assertEqual(url, "/employees/1/")

		employee = Employee.objects.get(pk=1)
		self.assertEqual(employee.first_name, "Testing")
		self.assertEqual(employee.last_name, "Employee")
