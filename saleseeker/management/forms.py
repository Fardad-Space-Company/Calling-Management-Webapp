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
        labels = {
            'DealStatus': 'Deal Status',
            'CallDuration': 'Call Duration',
            'Email': 'Email Address',
            'Appointement_Date': 'Appointment Date',
            'OWname': 'Owner Name',
            'OWnum': 'Owner Phone Number',
            'GKname': 'Gatekeeper Name',
            'GKnum': 'Gatekeeper Phone Number',
            'Note': 'Additional Notes',
            'Shop_Status': 'Shop Status'
        }
        widgets = {
            'CallDuration': forms.TextInput(attrs={'type': 'text', 'placeholder': 'HH:MM:SS'}),
            
        }
