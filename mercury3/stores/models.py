from django.db import models

class Store(models.Model):
	name = models.CharField(max_length=32)

class Location(models.Model):
	store = models.ForeignKey('Store', on_delete=models.CASCADE)
	name = models.CharField(max_length=8)