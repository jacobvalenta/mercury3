from django.views.generic import ListView

from .models import Log

class LogListView(ListView):
	model = Log
	template_name = "logs/list.html"