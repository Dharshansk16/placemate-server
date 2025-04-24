from django.db import models
from django.utils.text import slugify

class TechStack(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="companies")
    last_updated = models.DateTimeField(auto_now=True)

    # New fields for insights
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    average_ctc = models.FloatField(blank=True, null=True, help_text="Average CTC for freshers in LPA")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Role(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='roles')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="roles")

    # New fields for insights
    average_ctc = models.FloatField(blank=True, null=True, help_text="CTC for this role in LPA")
    job_location = models.CharField(max_length=255, blank=True, null=True)
    openings_per_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"


DIFFICULTY_LEVELS = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class InterviewExperience(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interview_experiences')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.TextField(blank=True)
    outcome = models.CharField(max_length=50, choices=[('selected', 'Selected'), ('rejected', 'Rejected')], blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='interview_experiences')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview at {self.company.name} for {self.role.title if self.role else 'Unknown Role'}"


class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(help_text="Rating out of 5", blank=True, null=True)
    review_text=models.TextField(blank=True)
    pros = models.TextField(blank=True, null=True)
    cons = models.TextField(blank=True, null=True)
    work_life_balance = models.IntegerField(blank=True, null=True, help_text="Rating out of 10")
    culture = models.IntegerField(blank=True, null=True, help_text="Rating out of 10")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.company.name} by {self.reviewer_name or 'Anonymous'}"
