from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm

class ImageUploadForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Add an email field to handle the email updates
    password = forms.CharField(widget=forms.PasswordInput(), required=False)  # Add a password field
    rule = forms.CharField(required=False)  # Add a rule field

    class Meta:
        model = Profile
        fields = ['image', 'email', 'password', 'rule']  # Update fields to include 'password' and 'rule'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            # Assuming you want to keep password and rule hidden or not prefilled
            # self.fields['password'].initial = user.profile.password
            # self.fields['rule'].initial = user.profile.rule

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.save()
        # Handle password update securely
        if self.cleaned_data['password']:
            self.instance.password = make_password(self.cleaned_data['password'])
        # Save rule text
        if self.cleaned_data['rule']:
            self.instance.rule = self.cleaned_data['rule']
        return super(ImageUploadForm, self).save(*args, **kwargs)
