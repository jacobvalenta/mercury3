from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView

from .forms import UserForm, EmployeeForm
from .models import Employee


class EmployeeFormsMixin(object):
	def get_user_form(self):
		"""
		Returns the `user_form` attribute if it is already set,
		otherwise it instanciates a new `UserForm` with appropriate
		data.
		"""

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
		"""
		Returns the `employee_form` attribute if it is already set,
		otherwise it instanciates a new `EmployeeForm` with appropriate
		data.
		"""

		try:
			return self.employee_form
		except AttributeError:
			try:
				employee = self.get_object()
			except AttributeError:
				employee = None

			if self.request.POST:
				if employee:
					self.employee_form = EmployeeForm( \
						self.request.POST,
						instance=employee)
				else:
					self.employee_form = EmployeeForm(self.request.POST)
			else:
				if employee:
					self.employee_form = EmployeeForm(instance=employee)
				else:
					self.employee_form = EmployeeForm()
		return self.employee_form

	def post(self, request, pk=None):
		user_form = self.get_user_form()
		employee_form = self.get_employee_form()

		if user_form.is_valid() and employee_form.is_valid():
			first_name = employee_form.cleaned_data['first_name']
			last_name = employee_form.cleaned_data['last_name']

			user = user_form.save(first_name, last_name)

			employee = employee_form.save(user, commit=False)
			
			# Maybe move _history_user assignment to models.py?
			employee._history_user = request.user
			employee.save()

			success_url = reverse('employees:detail',
			                      kwargs={'pk': employee.pk})
			return HttpResponseRedirect(success_url)
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


class EmployeeListView(ListView):
	model = Employee
	template_name = "employees/list.html"


class EmployeeCreateView(EmployeeFormsMixin, TemplateView):
	"""A view which subclasses `EmployeeFormsMixin` to validate
	   and save two forms."""

	model = Employee
	template_name = "employees/create.html"


class EmployeeUpdateView(EmployeeFormsMixin, DetailView):
	"""A view which subclasses `EmployeeFormsMixin` to validate
	   and save two forms."""
	model = Employee
	template_name = "employees/update.html"


class EmployeeDetailView(DetailView):
	model = Employee
	template_name = "employees/detail.html"