from django.contrib.postgres.search import SearchVector
from django.http import (HttpResponseBadRequest, HttpResponseRedirect,
						 Http404, JsonResponse)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView

from extra_views import ModelFormSetView

from .forms import ItemScanForm, SetItemLocationForm
from .models import Item, InventoryAudit

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

class SetItemLocationView(UpdateView):
	template_name = "items/set_location.html"
	form_class = SetItemLocationForm
	queryset = Item.objects.all()

	def get_success_url(self):
		return reverse("items:detail", kwargs={"pk": self.kwargs['pk']})

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		data.update({
			'pk': self.kwargs['pk']
		})
		return data

class LocationAssignmentView(ModelFormSetView):
	model = Item
	factory_kwargs = {'extra': 0}
	queryset = Item.objects.filter(location=None)
	form_class = SetItemLocationForm
	template_name = "items/location_assignment.html"
	# succes_url = reverse_lazy("main-page")

	def formset_valid(self, formset):
		print("formset valid")
		for form in formset:
			form.save()

		return HttpResponseRedirect(reverse("items:location-assignment"))

	# def formset_invalid(self, formset):
	# 	print("Invalid")
	# 	print(formset)

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)

		items = self.queryset

		items_and_forms_zipped = zip(items, data['formset'])

		data.update({
			'items_and_forms_zipped': items_and_forms_zipped,
			'items_count': items.count()
		})
		return data

class InventoryAuditView(TemplateView):

	def get_last_audit(self):
		last_audit = InventoryAudit.objects.filter( \
			time_end__isnull=False).order_by('-time_end').first()

		return last_audit

	def get_audit(self):
		try:
			return self.current_audit
		except AttributeError:
			try:
				self.current_audit = InventoryAudit.objects.get(time_end=None)
			except InventoryAudit.DoesNotExist:
				self.current_audit = None
			return self.current_audit

	def get_template_names(self, *args, **kwargs):
		audit = self.get_audit()
		
		if audit:
			return "items/inventory_audit_in_progress.html"
		else:
			return "items/inventory_audit.html"

	def post(self, *args, **kwargs):
		if self.get_audit():
			return HttpResponseBadRequest("Audit already in progress.")

		audit = InventoryAudit()
		audit.save()

		return HttpResponseRedirect(reverse('items:inventory-audit'))

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)

		audit = self.get_audit()
		last_audit = self.get_last_audit()

		print("Last audit:", last_audit)

		if last_audit:
			last_audit_ago = (timezone.now() - last_audit.time_end).days
		else:
			last_audit_ago = None

		data.update({
			'audit': audit,
			'last_audit': last_audit,
			'last_audit_ago': last_audit_ago
		})

		return data


class InventoryAuditDetailView(DetailView):
	model = InventoryAudit
	template_name = "items/inventory_audit_detail.html"

	def get_last_audit(self):
		last_audit = InventoryAudit.objects.filter( \
			time_end__isnull=False).order_by('-time_end').first()


		return last_audit

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		last_audit = self.get_last_audit()

		data.update({
			'most_recent_audit': self.get_object() == last_audit
		})

		return data

@require_http_methods(["POST"])
def audit_scan_item_view(request):
	try:
		audit = InventoryAudit.objects.get(time_end=None)
	except InventoryAudit.DoesNotExist:
		HttpResponseBadRequest('No inventory in progress.')

	form = ItemScanForm(request.POST, audit=audit)
	if form.is_valid():
		item = form.cleaned_data['item']
		audit.items_left.remove(item)
		return JsonResponse({'success': True})
	else:
		return JsonResponse({'error': True})

@require_http_methods(["POST"])
def audit_finish(request):
	try:
		audit = InventoryAudit.objects.get(time_end=None)
	except InventoryAudit.DoesNotExist:
		return HttpResponseBadRequest('No inventory in progress.')

	audit.time_end = timezone.now()
	audit.save()

	return HttpResponseRedirect(reverse('items:inventory-audit-detail',
								kwargs={'pk': audit.pk}))

@require_http_methods(["POST"])
def audit_reopen_view(request, pk):
	try:
		audit = InventoryAudit.objects.get(pk=pk)
	except InventoryAudit.DoesNotExist:
		raise Http404

	try:
		last_audit = InventoryAudit.objects.filter( \
			time_end__isnull=False).order_by('-time_end').first()
	except InventoryAudit.DoesNotExist:
		return HttpResponseBadRequest('No inventories exist')

	if last_audit == audit:
		audit.time_end = None
		audit.save()
	else:
		return HttpResponseBadRequest("Trying to reopen an old audit")

	return HttpResponseRedirect(reverse('items:inventory-audit'))

@require_http_methods(["POST"])
def audit_make_missing_items_view(request, pk):
	try:
		audit = InventoryAudit.objects.get(pk=pk)
	except InventoryAudit.DoesNotExist:
		raise Http404

	for item in audit.items_left.all():
		item.status = Item.MISSING
		item.save()

	return HttpResponseRedirect(reverse('items:inventory-audit'))

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