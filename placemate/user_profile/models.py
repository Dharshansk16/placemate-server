from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Skill(models.Model):
    """
    Represents a specific technical or non-technical skill (e.g., Python, Public Speaking).
    Used to enhance recommendation and filtering.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobInterest(models.Model):
    """
    Represents a type of job or domain a user is interested in (e.g., Backend Developer, Data Analyst).
    """
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
    Extends the base User model with additional profile data.
    Stores personal and academic details that help personalize the Placemate experience.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.URLField(blank=True, null=True) 

    # Fields used for smart matching and suggestions
    skills = models.ManyToManyField(Skill, blank=True) 
    job_interests = models.ManyToManyField(JobInterest, blank=True) 
    bio = models.TextField(blank=True) 
    education = models.CharField(max_length=255, blank=True) 
    experience = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)  
    def save(self, *args, **kwargs):
        """
        Auto-generates slug from username if not set.
        """
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
