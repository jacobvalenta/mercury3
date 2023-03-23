from django.apps import apps
from django.db import models, IntegrityError
from django.utils import timezone

class DrawerIdentifierManager(models.Manager):
    def not_open(self):
    	open_drawer_identifiers = self.filter(drawer__is_open=True)
    	open_pks = open_drawer_identifiers.values_list("pk", flat=True)

    	return self.exclude(pk__in=open_pks)


class DrawerIdentifier(models.Model):
	name = models.CharField(max_length=14)

	objects = DrawerIdentifierManager()

	def __str__(self):
		return self.name

class Drawer(models.Model):
	identifier_key = models.ForeignKey(DrawerIdentifier, blank=True,
	                                   null=True, on_delete=models.PROTECT)

	balance = models.DecimalField(max_digits=9, decimal_places=2)

	is_open = models.BooleanField(default=True)

	opened_by = models.ForeignKey('employees.Employee',
	                              related_name="opening_employee",
								  on_delete=models.PROTECT)
	closed_by = models.ForeignKey('employees.Employee',
	                              related_name="closing_employee",
	                              blank=True, null=True,
								  on_delete=models.PROTECT)

	opened_at = models.DateTimeField(auto_now_add=True)
	closed_at = models.DateTimeField(blank=True, null=True)

	# changed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

	def __str__(self):
		return "#{}: ${}".format(self.identifier, self.balance)

	@property
	def identifier(self):
		if self.identifier_key:
			return self.identifier_key.name
		else:
			return str(self.pk)

	def close(self, user):
		Log = apps.get_model('logs.Log')

		self.closed_by = user.employee
		self.closed_at = timezone.now()
		self.is_open = False

		msg_template = "closed a Drawer ({}) with $@protected({})."
		msg = msg_template.format(self.identifier, self.balance)
		Log.objects.create(user=user, message=msg)

		self.save(user)

	def save(self, user, **kwargs):
		Log = apps.get_model('logs.Log')

		if not self.pk:
			# Check to make sure there are no open drawers
			# (with this identifier).
			if self.identifier_key:
				number_of_open_drawers_with_this_identifier = \
					Drawer.objects.filter(is_open=True,
					                      identifier_key=self.identifier_key)

				if len(number_of_open_drawers_with_this_identifier) > 0:
					msg = "Drawer already open with this identifier."
					raise IntegrityError(msg)

			# Log Drawer creation
			msg_template = "opened a Drawer ({}) with $@protected({})."
			msg = msg_template.format(self.identifier, self.balance)
			Log.objects.create(user=user, message=msg)

		super().save(**kwargs)