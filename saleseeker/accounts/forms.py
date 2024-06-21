from django import forms
from .models import Profile

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
