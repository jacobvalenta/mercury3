from decimal import Decimal

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from mercury3.items.forms import ItemForm

from .forms import TransactionForm, TransactionItemForm
from .models import Transaction, TransactionItem

class TransactionCreateView(TemplateView):
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

			transaction = self.form.save(item_data=item_data)

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
				item.status = Item.HOLD
				item.save()
				item_data.append({'item': item, 'price': item.price_in})

			transaction = self.form.save(item_data=item_data)

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


class TransactionDetailView(DetailView):
	template_name = "transactions/detail.html"
	model = Transaction