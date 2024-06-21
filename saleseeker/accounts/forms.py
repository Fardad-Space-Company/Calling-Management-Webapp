from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    rule = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'rule', 'email'] 
