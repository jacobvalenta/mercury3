from django.views.generic.edit import CreateView

from .models import Transaction

class TransactionCreateView(CreateView):
	template_name = "transactions/create.html"
	model = Transaction
	fields = ["customer", "items"]