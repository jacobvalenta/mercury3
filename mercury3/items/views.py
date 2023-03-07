from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.views.generic import TemplateView, DetailView

from .models import Item

class ItemSearchView(TemplateView):
	template_name = "items/search.html"

	def post(self, request):
		query = request.POST.get('q', None)
		results = []

		if query:
			vector = SearchVector('make') + SearchVector('model') + \
					 SearchVector('pk')
			items = Item.objects.annotate(search=vector).filter(search__icontains=query)
			for item in items:
				results.append({'pk': item.pk, 'make': item.make,
								'model': item.model,
								'absolute_url': item.get_absolute_url()})

		return JsonResponse(results, safe=False)

class ItemDetailView(DetailView):
	template_name = "items/detail.html"
	model = Item

def search_item_number_ajax_view(request):
	query = request.POST.get('q', None)

	if not query:
		return HttpResponseBadRequest()

	try:
		item = Item.objects.get(pk=query)
		result = {'pk': str(item.pk).zfill(7), 'make': item.make, 'model': item.model, 'price': item.price}
		return JsonResponse(result)
	except Item.DoesNotExist:
		raise Http404()