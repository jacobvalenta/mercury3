from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.views.generic import TemplateView

from .models import Item

class ItemSearch(TemplateView):
	template_name = "items/search.html"

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