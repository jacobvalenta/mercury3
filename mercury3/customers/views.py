from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from mercury3.utils import is_number

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
		query = request.POST.get('q', None).strip()
		results = []

		if query:
			query_split = query.split()

			if query_split[0] and is_number(query_split[0]):
				customers = Customer.objects.filter( \
					Q(address_1__icontains=query) | \
					Q(phone_number__icontains=query)).order_by('-pk')
			else:
				if len(query_split) == 1:
					customers = Customer.objects.filter( \
						Q(first_name__icontains=query) | \
						Q(last_name__icontains=query)).order_by('-pk')

				elif len(query_split) == 2:
					customers = Customer.objects.filter( \
						first_name__icontains=query_split[0],
						last_name__icontains=query_split[1]).order_by('-pk')

				elif len(query_split) == 3:
					customers = Customer.objects.filter( \
						first_name__icontains=query_split[0], \
						middle_name__icontains=query_split[1], \
						last_name__icontains=query_split[2]).order_by('-pk')

			for customer in customers:
				results.append({'pk': customer.pk, 'full_name': customer.full_name, 'address_1': customer.address_1, 'absolute_url': customer.get_absolute_url()})

		return JsonResponse(results, safe=False)