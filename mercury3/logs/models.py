from django.contrib.auth.models import User
from django.db import models

class Log(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	message = models.CharField(max_length=250)

	timestamp = models.DateTimeField(auto_now_add=True)