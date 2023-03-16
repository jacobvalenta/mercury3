from django.db import models

from mercury3.core.models import Plan

class PawnLoan(Plan):
	pass

	@property
	def redeem_amount(self):
		return self.principle_amount + self.amount_due