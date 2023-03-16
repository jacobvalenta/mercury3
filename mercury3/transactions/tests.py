from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from mercury3.customers.models import Customer
from mercury3.items.models import Item
from mercury3.pawn_loans.models import PawnLoan

from .models import Transaction

class TransactionTestCase(TestCase):
	fixtures = ["customers_test.json"]

    # def setUp(self):
    #     Customer.objects.create(first_name="test", last_name="customer")
    #     Animal.objects.create(name="cat", sound="meow")

	def get_pk_from_url(self, url):
		try:
			return int(url.split('/')[2])
		except IndexError:
			return None
		except ValueError:
			return None

	def test_in_transaction_200(self):
		"""Test In Transaction"""
		response = self.client.get(reverse('transactions:create-in'))
		self.assertEqual(response.status_code, 200)

	def test_out_transaction_200(self):
		"""Test Out Transaction"""
		response = self.client.get(reverse('transactions:create-out'))
		self.assertEqual(response.status_code, 200)

	def test_buy_transaction(self):
		"""Tests buy transactions. Tests: response is a redirect,
		`transaction_type` equals "buy", creation time less than
		2 seconds ago, and item placed in hold."""

		post_data = {
			'customer': 1, 
			'form-0-make': "Apple",
			'form-0-model': "iPhone",
			'form-0-price_in': "1.00",
			'form-INITIAL_FORMS': 0,
			'form-TOTAL_FORMS': 1,
			'transaction_type': 'buy'
		}

		# Response is a redirect
		response = self.client.post(reverse('transactions:create-in'),
									post_data)
		self.assertEqual(response.status_code, 302)

		pk = self.get_pk_from_url(response.headers['Location'])

		# `transaction_type` equals "buy"
		transaction = Transaction.objects.get(pk=pk)
		self.assertEqual(transaction.transaction_type, transaction.BUY)

		# Creation time less than 2 seconds ago.
		ago = (timezone.now() - transaction.timestamp).microseconds
		self.assertLess(ago, 2000000)

		# Items placed in hold.
		for item in transaction.items.all():
			self.assertEqual(item.status, Item.HOLD)

	def test_pawn_transaction(self):
		post_data = {
			'customer': 1, 
			'form-0-make': "Apple",
			'form-0-model': "iPhone",
			'form-0-price_in': "1.00",
			'form-INITIAL_FORMS': 0,
			'form-TOTAL_FORMS': 1,
			'transaction_type': 'pawn'
		}

		response = self.client.post(reverse('transactions:create-in'),
									post_data)
		self.assertEqual(response.status_code, 302)

		pk = self.get_pk_from_url(response.headers['Location'])

		transaction = Transaction.objects.get(pk=pk)
		self.assertEqual(transaction.transaction_type, transaction.PAWN)

		# Creation time less than 2 seconds ago.
		ago = (timezone.now() - transaction.timestamp).microseconds
		self.assertLess(ago, 2000000)

		for item in transaction.items.all():
			self.assertEqual(item.status, Item.PAWN)

		pawn_loan = PawnLoan.objects.get(pk=1)
		self.assertEqual(pawn_loan.principle_amount, Decimal(1.00))