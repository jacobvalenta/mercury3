from django.db import models

class Drawer(models.Model):
	number = models.PositiveIntegerField(blank=True, null=True)

	balance = models.DecimalField(max_digits=9, decimal_places=2)

	is_open = models.BooleanField(default=True)

	opened_by = models.ForeignKey('employees.Employee',
								  on_delete=models.PROTECT)
	opened_at = models.DateTimeField(auto_now_add=True)
	closed_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		identifier = str(self.number) if self.number else str(self.pk)
		identifier = identifier.zfill(3)

		return "#{}: ${}".format(identifier, self.balance)