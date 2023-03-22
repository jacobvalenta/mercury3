from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import OpenDrawerForm, CloseDrawerForm
from .models import Drawer

class OpenDrawerView(CreateView):
	form_class = OpenDrawerForm
	template_name = "drawers/open.html"
	success_url = reverse_lazy("main-page")

	def form_valid(self, form):
		drawer = form.save(commit=False)
		drawer.opened_by = self.request.user.employee

		drawer.save()

		return HttpResponseRedirect(self.get_success_url())

class CloseDrawerView(UpdateView):
	model = Drawer
	form_class = CloseDrawerForm
	template_name = "drawers/close.html"
	success_url = reverse_lazy("main-page")

	def form_valid(self, form):
		drawer = form.save()
		
		return HttpResponseRedirect(self.get_success_url())

class DrawerListView(ListView):
	model = Drawer
	queryset = Drawer.objects.filter(is_open=True)
	template_name = "drawers/list.html"