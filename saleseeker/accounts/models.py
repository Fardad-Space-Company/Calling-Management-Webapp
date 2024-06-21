from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    rule = models.CharField(max_length=100, default='Default Rule')
    email = models.EmailField(max_length=100, blank=True)
    # Extra password field, use cautiously considering security practices

    def __str__(self):
        return f'{self.user.username} Profile'