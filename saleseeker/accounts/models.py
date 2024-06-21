from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    rule = models.CharField(max_length=100, default='Default Rule')
    # Extra password field, use cautiously considering security practices
    password = models.CharField(max_length=255, default='1234')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Ensuring the password is hashed before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
