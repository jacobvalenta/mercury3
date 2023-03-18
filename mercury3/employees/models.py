from django.db import models

class Employee(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

	store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)