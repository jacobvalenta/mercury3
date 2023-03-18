from django.db import models

class Employee(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

	store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)

	def __str__(self):
		return "{0} {1}".format(self.user.first_name, self.user.last_name)