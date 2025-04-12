from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class JobInterest(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for smart recommendations 
    skills = models.ManyToManyField(Skill, blank=True)
    job_interests = models.ManyToManyField(JobInterest, blank=True)
    bio = models.TextField(blank=True)
    education = models.CharField(max_length=255, blank=True)
    experience = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name