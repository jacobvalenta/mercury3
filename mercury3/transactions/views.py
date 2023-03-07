from decimal import Decimal

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

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
			item_data = [{'item': i.cleaned_data['item'],
						  'price': i.cleaned_data['price']} \
				for i in self.formset]

			transaction = self.form.save(item_data=item_data)

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

class TransactionDetailView(DetailView):
	template_name = "transactions/detail.html"
	model = Transaction