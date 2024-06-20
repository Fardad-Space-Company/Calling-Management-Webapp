from django import forms
from .models import CRMbackend
class CRMbackendForm(forms.ModelForm):
    class Meta:
        model = CRMbackend
        fields = [
            'DealStatus', 
            'CallDuration', 
            'Email', 
            'Appointement_Date', 
            'OWname', 
            'OWnum', 
            'GKname', 
            'GKnum', 
            'Note', 
            'Shop_Status'
        ]

