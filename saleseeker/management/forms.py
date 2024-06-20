from django import forms
from .models import CRMbackend
class CRMbackendForm(forms.ModelForm):
    class Meta:
        model = CRMbackend
        fields = [
            'EmployeeID', 
            'DealStatus', 
            # 'ShopName', 
            # 'Date', 
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

        widgets = {
            'EmployeeID': forms.TextInput(attrs={'max_length': 11, 'required': True}),
            'DealStatus': forms.TextInput(attrs={'max_length': 20, 'required': True}),
            'CallDuration': forms.Textarea(attrs={'required': False}),
            'Email': forms.TextInput(attrs={'max_length': 50, 'required': False}),
            'Appointement_Date': forms.Textarea(attrs={'required': False}),
            'OWname': forms.TextInput(attrs={'max_length': 20, 'required': False}),
            'OWnum': forms.TextInput(attrs={'max_length': 15, 'required': False}),
            'GKname': forms.TextInput(attrs={'max_length': 20, 'required': False}),
            'GKnum': forms.TextInput(attrs={'max_length': 15, 'required': False}),
            'Note': forms.Textarea(attrs={'required': False}),
            'Shop_Status': forms.TextInput(attrs={'max_length': 20, 'required': True}),
        }

