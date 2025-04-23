from django.db import models
from django.utils.text import slugify

class TechStack(models.Model):
    """
    Represents a single technology or tool (e.g., Python, React, Docker).
    """
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    """
    Represents a company that hires students. Each company can have multiple roles and use multiple technologies.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Auto-generated from the name
    description = models.TextField(blank=True, null=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="companies")  # General tech used by company

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Auto-create slug if not set
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Represents a job role offered by a company.
    Each role can have a role-specific tech stack (in addition to the company's general stack).
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='roles')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="roles")  # Tech required for this specific role

    def __str__(self):
        return f"{self.title} at {self.company.name}"


DIFFICULTY_LEVELS = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class InterviewExperience(models.Model):
    """
    Represents a student's interview experience for a specific company and role.
    Optionally tagged with outcome, difficulty level, and specific tech stack discussed in the interview.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interview_experiences')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)  # Optional if role not specified
    experience = models.TextField(blank=True)  # Full text of the interview experience
    outcome = models.CharField(max_length=50, choices=[('selected', 'Selected'), ('rejected', 'Rejected')], blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='interview_experiences')  # Tools/Tech discussed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview at {self.company.name} for {self.role.title if self.role else 'Unknown Role'}"
