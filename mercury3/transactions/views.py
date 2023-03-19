from decimal import Decimal

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView

from mercury3.items.forms import ItemForm
from mercury3.items.models import Item
from mercury3.pawn_loans.models import PawnLoan

from .forms import TransactionForm, TransactionItemForm, PayOrRedeemPawnForm
from .models import Transaction, TransactionItem


class InTransactionCreateView(TemplateView):
	template_name = "transactions/create_in.html"

	def get(self, request):
		self.form = TransactionForm()
		ItemFormSet = formset_factory(ItemForm)
		self.formset = ItemFormSet(request.POST)

		return super().get(request)

	def post(self, request):
		self.form = TransactionForm(request.POST)
		ItemFormSet = formset_factory(ItemForm)
		self.formset = ItemFormSet(request.POST)

		if self.formset.is_valid() and self.form.is_valid():
			item_data = []

			for item_form in self.formset:
				item = item_form.save(commit=False)
				if self.form.cleaned_data['transaction_type'] == "buy":
					item.status = Item.HOLD
				elif self.form.cleaned_data['transaction_type'] == "pawn":
					item.status = Item.PAWN
				item.save()
				item_data.append({'item': item, 'price': item.price_in})

			transaction = self.form.save(item_data=item_data, user=request.user)

			return HttpResponseRedirect(reverse('transactions:detail',
						   kwargs={'pk': transaction.pk}))

		else:
			return TemplateResponse(request, 'transactions/create_in.html',
									self.get_context_data())

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		data.update({
			'form': self.form,
			'item_formset': self.formset
		})
		return data


class OutTransactionCreateView(TemplateView):
	template_name = "transactions/create.html"

	def get(self, request):
		self.form = TransactionForm()
		ItemFormSet = formset_factory(TransactionItemForm)
		self.formset = ItemFormSet(request.POST)

		return super().get(request)

	def post(self, request):
		self.form = TransactionForm(request.POST)
		ItemFormSet = formset_factory(TransactionItemForm)
		self.formset = ItemFormSet(request.POST)

		if self.formset.is_valid() and self.form.is_valid():
			item_data = []

			for item_form in self.formset:
				item_data.append({'item': item_form.cleaned_data['item'],
								  'price': item_form.cleaned_data['price']})

			transaction = self.form.save(item_data=item_data,
										 user=request.user)

			for item in [i['item'] for i in item_data]:
				if transaction.transaction_type == Transaction.SALE:
					item.status = "SOLD"
					item.save()
				elif transaction.transaction_type == Transaction.LAYAWAY:
					raise NotImplemented("Layaway transactions not available")

			return HttpResponseRedirect(reverse('transactions:detail',
						   kwargs={'pk': transaction.pk}))

		else:
			return TemplateResponse(request, 'transactions/create.html',
									self.get_context_data())

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		data.update({
			'form': self.form,
			'item_formset': self.formset
		})
		return data


class PayOrRedeemPawnView(FormView):
	form_class = PayOrRedeemPawnForm
	template_name = 'transactions/pay_or_redeem.html'

	def get_success_url(self):
		return reverse('transactions:detail',
					   kwargs={'pk': self.transaction.pk})

	def form_valid(self, form):
		self.transaction = form.save(user=self.request.user)
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		data.update({
			'transaction_type': self.kwargs['type']
		})

		if self.request.GET.get('loan'):
			loan_pk = self.request.GET.get('loan')
			pawn_loan = PawnLoan.objects.get(pk=loan_pk)

			data.update({
				'customer': pawn_loan.customer,
				'pawn_loan': pawn_loan
			})

		return data

class TransactionDetailView(DetailView):
	template_name = "transactions/detail.html"
	model = Transaction