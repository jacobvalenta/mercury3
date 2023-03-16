from django.test import TestCase
from django.urls import reverse

from mercury3.customers.models import Customer

from .models import Transaction

class TransactionTestCase(TestCase):
	fixtures = ["customers_test.json"]

    # def setUp(self):
    #     Customer.objects.create(first_name="test", last_name="customer")
    #     Animal.objects.create(name="cat", sound="meow")

	def test_in_transaction_200(self):
		"""Test In Transaction"""
		response = self.client.get(reverse('transactions:create-in'))
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, "No polls are available.")
		# self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_out_transaction_200(self):
		"""Test Out Transaction"""
		response = self.client.get(reverse('transactions:create-out'))
		self.assertEqual(response.status_code, 200)

	def test_buy_transaction(self):
		post_data = {
			'customer': 1, 
			'form-0-make': "Apple",
			'form-0-model': "iPhone",
			'form-0-price_in': "1.00",
			'form-INITIAL_FORMS': 0,
			'form-TOTAL_FORMS': 1,
			'transaction_type': 'buy'
		}

		response = self.client.post(reverse('transactions:create-in'),
									post_data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.headers['Location'], "/transactions/1/")

		transaction = Transaction.objects.get(pk=1)
		self.assertEqual(transaction.transaction_type, transaction.BUY)