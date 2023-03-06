from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Customer

class CustomerCreateView(CreateView):
	template_name = "customers/customer_create.html"
	model = Customer
	fields = ["first_name", "middle_name", "last_name", "address_1", "address_2", "city", "state", "zip_code", "phone_number"]
	
class CustomerDetailView(DetailView):
	template_name = "customers/customer_detail.html"
	model = Customer
	pk_url_kwarg = "customer_pk"

class CustomerSearchView(TemplateView):
	template_name = "customers/customer_search.html"

	def post(self, request):
		query = request.POST.get('q', None)
		results = []

		if query:
			vector = SearchVector('first_name', weight='B') + SearchVector('middle_name', weight="D") + SearchVector('last_name', weight='A') + SearchVector('address_1', weight="C") + SearchVector('address_2', weight="C") + SearchVector('phone_number', weight="B")
			customers = Customer.objects.annotate(rank=vector).filter(rank__icontains=query).order_by("-rank")
			for customer in customers:
				results.append({'rank': customer.rank, 'pk': customer.pk, 'full_name': customer.get_full_name(), 'absolute_url': customer.get_absolute_url()})

		return JsonResponse(results, safe=False)