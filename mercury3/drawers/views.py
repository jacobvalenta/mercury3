from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Drawer

class OpenDrawerView(CreateView):
	model = Drawer
	fields = ["number", "balance"]
	template_name = "drawers/open_drawer.html"
	success_url = reverse_lazy("main-page")

	def form_valid(self, form):
		print("Form Valid")

		drawer = form.save(commit=False)
		drawer.opened_by = self.request.user.employee

		drawer.save()

		return super().form_valid(form)