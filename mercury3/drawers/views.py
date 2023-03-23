from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import OpenDrawerForm, CloseDrawerForm
from .models import Drawer

class OpenDrawerView(CreateView):
	form_class = OpenDrawerForm
	template_name = "drawers/open.html"
	
	def get_success_url(self):
		return reverse("main-page")

	def form_valid(self, form):
		drawer = form.save(commit=False)
		drawer.opened_by = self.request.user.employee

		drawer.save(user=self.request.user)

		return HttpResponseRedirect(self.get_success_url())

class CloseDrawerView(UpdateView):
	model = Drawer
	form_class = CloseDrawerForm
	template_name = "drawers/close.html"

	def get_success_url(self):
		return reverse("main-page")

	def form_valid(self, form):
		drawer = form.save(user=self.request.user)
		
		return HttpResponseRedirect(self.get_success_url())

class DrawerListView(ListView):
	model = Drawer
	queryset = Drawer.objects.filter(is_open=True)
	template_name = "drawers/list.html"