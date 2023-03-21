from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView

from .forms import UserForm, EmployeeForm
from .models import Employee


class EmployeeFormsMixin(object):
	def get_user_form(self):
		try:
			return self.user_form
		except AttributeError:
			try:
				instance = self.get_object()
			except AttributeError:
				instance = None
			if self.request.POST:
				self.user_form = UserForm(self.request.POST,
										  instance=instance)
			else:
				self.user_form = UserForm()
		return self.user_form

	def get_employee_form(self):
		print("Here")

		try:
			return self.employee_form
		except AttributeError:
			try:
				employee = self.get_object()
			except AttributeError:
				employee = None

			if employee:
				initial = {'first_name': employee.first_name,
					       'last_name': employee.last_name,
					       'store': employee.store}
			else:
				initial = {}

			if self.request.POST:
				self.employee_form = EmployeeForm( \
					self.request.POST,
					instance=employee,
					initial=initial)
			else:
				if initial:
					self.employee_form = EmployeeForm(initial=initial)
				else:
					self.employee_form = EmployeeForm()
		return self.employee_form

	def post(self, request, pk=None):
		user_form = self.get_user_form()
		employee_form = self.get_employee_form()

		if user_form.is_valid() and employee_form.is_valid():
			first_name = employee_form.cleaned_data['first_name']
			last_name = employee_form.cleaned_data['last_name']

			if pk:
				user = user_form.save()
			else:
				user = user_form.save(first_name=first_name, last_name=last_name)

			employee = employee_form.save(user, commit=False)
			
			employee._history_user = request.user
			employee.save()

			return HttpResponseRedirect(reverse('employees:detail',
												kwargs={'pk': employee.pk}))
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


class EmployeeManagementView(TemplateView):
	template_name = "employees/manage.html"


class EmployeeCreateView(EmployeeFormsMixin, TemplateView):
	"""A view which subclasses EmployeeFormsMix to validate
	   and save two forms."""

	model = Employee
	template_name = "employees/create.html"

class EmployeeListView(ListView):
	model = Employee
	template_name = "employees/list.html"


class EmployeeDetailView(DetailView):
	model = Employee
	template_name = "employees/detail.html"

class EmployeeUpdateView(EmployeeFormsMixin, DetailView):
	"""A view which subclasses EmployeeFormsMix to validate
	   and save two forms."""
	model = Employee
	template_name = "employees/update.html"
