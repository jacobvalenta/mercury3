from django.apps import apps
from django.db import models

from simple_history.models import HistoricalRecords

class Employee(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)

	store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)

	changed_by = models.ForeignKey('auth.User',
								   on_delete=models.PROTECT,
								   related_name="changed_by")

	changed_at = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	def __str__(self):
		return "{0} {1}".format(self.first_name, self.last_name)

	def save(self, user, **kwargs):
		Log = apps.get_model('logs.Log')
		created = False
		
		if not self.pk:
			created = True

		self._history_user = user

		super().save(**kwargs)

		if created:
			log = Log(user=self._history_user,
				message="created Employee ({0})".format(str(self)))
			log.save()
		else:
			log = Log(user=self._history_user,
				message="edited Employee ({0})".format(str(self)))
			log.save()


	@property
	def _history_user(self):
		return self.changed_by

	@_history_user.setter
	def _history_user(self, value):
		self.changed_by = value

	@property
	def _history_date(self):
		return self.changed_at

	@_history_date.setter
	def _history_date(self, value):
		self.changed_at = value