from django.views.generic import DetailView

from .models import PawnLoan

class PawnLoanDetailView(DetailView):
	model = PawnLoan
	template_name = "pawn_loans/detail.html"