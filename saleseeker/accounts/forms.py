from django import forms
from .models import Profile

# class ProfileUpdateForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     rule = forms.CharField(required=False)

#     class Meta:
#         model = Profile
#         fields = ['image', 'rule', 'email'] 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'rule']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']