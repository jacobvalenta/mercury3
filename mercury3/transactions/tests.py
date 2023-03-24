from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from mercury3.customers.models import Customer
from mercury3.items.models import Item
from mercury3.pawn_loans.models import PawnLoan
from mercury3.utils import TWO_SECONDS, get_pk_from_url

from .models import Transaction

class TransactionTestCase(TestCase):
	fixtures = ["stores_test.json", "drawers_test.json",
				"customers_test.json", "employees_test.json"]

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
			'drawer': 1,
			'transaction_type': 'buy'
		}

		# Response is a redirect
		self.client.login(username='temployee', password='brickandmortar')
		response = self.client.post(reverse('transactions:create-in'),
									post_data)
		self.assertEqual(response.status_code, 302)

		pk = get_pk_from_url(response.headers['Location'])

		# `transaction_type` equals "buy"
		transaction = Transaction.objects.get(pk=pk)
		self.assertEqual(transaction.transaction_type, transaction.BUY)

		# Creation time less than 2 seconds ago.
		ago = (timezone.now() - transaction.timestamp).microseconds
		self.assertLess(ago, TWO_SECONDS)

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
			'drawer': 1,
			'transaction_type': 'pawn'
		}

		# Response is a redirect
		url = reverse('transactions:create-in')
		self.client.login(username='temployee', password='brickandmortar')
		response = self.client.post(url, post_data)
		self.assertEqual(response.status_code, 302)

		pk = get_pk_from_url(response.headers['Location'])
		transaction = Transaction.objects.get(pk=pk)

		# `transaction_type` equals "buy"
		self.assertEqual(transaction.transaction_type, transaction.PAWN)

		# Creation time less than 2 seconds ago.
		ago = (timezone.now() - transaction.timestamp).microseconds
		self.assertLess(ago, TWO_SECONDS)

		# Items marked as pawn.
		for item in transaction.items.all():
			self.assertEqual(item.status, Item.PAWN)

		# Pawn loan has correct principle amount.
		pawn_loan = transaction.pawnloan_set.first()
		self.assertEqual(pawn_loan.principle_amount, Decimal(1.00))

	def test_redeem_transaction(self):
		pawn_post_data = {
			'customer': 1, 
			'form-0-make': "Apple",
			'form-0-model': "iPhone",
			'form-0-price_in': "1.00",
			'form-INITIAL_FORMS': 0,
			'form-TOTAL_FORMS': 1,
			'drawer': 1,
			'transaction_type': 'pawn'
		}

		# Response is a redirect
		pawn_url = reverse('transactions:create-in')
		self.client.login(username='temployee', password='brickandmortar')
		pawn_response = self.client.post(pawn_url, pawn_post_data)
		self.assertEqual(pawn_response.status_code, 302)

		pk = get_pk_from_url(pawn_response.headers['Location'])
		transaction = Transaction.objects.get(pk=pk)

		pawn_loan = transaction.pawnloan_set.first()

		redeem_post_data = {
			'customer': 1, 
			'pawn_loan': pawn_loan.pk,
			'payment_amount': pawn_loan.redeem_amount,
			'drawer': 1,
			'transaction_type': 'redeem'
		}
		redeem_url = reverse('transactions:pay')
		redeem_url += "?loan={0}".format(pawn_loan.pk)
		redeem_response = self.client.post(redeem_url, redeem_post_data)

		self.assertEqual(redeem_response.status_code, 302)

		pk = get_pk_from_url(redeem_response.headers['Location'])

		transaction = Transaction.objects.get(pk=pk)

		# `transaction_type` equals "buy"
		self.assertEqual(transaction.transaction_type, transaction.REDEEM)

		# Creation time less than 2 seconds ago.
		ago = (timezone.now() - transaction.timestamp).microseconds
		self.assertLess(ago, TWO_SECONDS)

		# Items marked as pawn.
		for item in transaction.items.all():
			self.assertEqual(item.status, Item.REDEEMED)

		# Pawn loan has correct principle amount.
		pawn_loan = transaction.pawnloan_set.first()
		self.assertEqual(pawn_loan.unpaid_principle, Decimal(0.00))
		self.assertEqual(pawn_loan.status, PawnLoan.REDEEMED)