from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import UserForm, EmployeeForm
from .models import Employee

class EmployeeManagementView(TemplateView):
	template_name = "employees/manage.html"

class EmployeeCreateView(TemplateView):
	model = Employee
	template_name = "employees/create.html"

	def get_user_form(self):
		try:
			return self.user_form
		except AttributeError:
			if self.request.POST:
				self.user_form = UserForm(self.request.POST)
			else:
				self.user_form = UserForm()
		return self.user_form

	def get_employee_form(self):
		try:
			return self.employee_form
		except AttributeError:
			if self.request.POST:
				self.employee_form = EmployeeForm(self.request.POST)
			else:
				self.employee_form = EmployeeForm()
		return self.employee_form

	def post(self, request):
		user_form = self.get_user_form()
		employee_form = self.get_employee_form()

		if user_form.is_valid() and employee_form.is_valid():
			user = user_form.save()
			employee = employee_form.save(user)

			return HttpResponseRedirect(reverse('employees:manage'))
		else:
			return TemplateResponse(request, self.get_template_names(),
									self.get_context_data())

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)

		data.update({
			'user_form': self.get_user_form(),
			'employee_form': self.get_employee_form()
		})

		return data