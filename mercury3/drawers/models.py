from django.db import models
from django.utils import timezone

class Drawer(models.Model):
	number = models.PositiveIntegerField(blank=True, null=True)

	balance = models.DecimalField(max_digits=9, decimal_places=2)

	is_open = models.BooleanField(default=True)

	opened_by = models.ForeignKey('employees.Employee',
								  on_delete=models.PROTECT)
	opened_at = models.DateTimeField(auto_now_add=True)
	closed_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return "#{}: ${}".format(self.identifier, self.balance)

	@property
	def identifier(self):
		identifier_str = str(self.number) if self.number else str(self.pk)
		identifier_str = identifier_str.zfill(3)

		return identifier_str

	def close(self):
		self.closed_at = timezone.now()
		self.is_open = False
		self.save()