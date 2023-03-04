from django.views.generic import TemplateView

from django.shortcuts import render

class MainPageView(TemplateView):
	template_name = "main_page.html"