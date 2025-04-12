from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_premium = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)  # Google-specific ID
    profile_picture = models.URLField(blank=True, null=True)  # Google profile image URL
    
    USERNAME_FIELD = 'email' #google auth returns email of the logged in user override username field with email
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username