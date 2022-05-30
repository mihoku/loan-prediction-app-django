from django import forms
from .models import ExecutingAgency, Lender, Loan 

class EAForm(forms.ModelForm):
    class Meta:
        model = ExecutingAgency
        fields = "__all__"

class LenderForm(forms.ModelForm):
    class Meta:
        model=Lender
        fields="__all__"

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = "__all__"