from django.contrib import admin
from .models import Company, TechStack, InterviewExperience, Role

# Register your models here.
admin.site.register(Company)
admin.site.register(TechStack)
admin.site.register(Role)
admin.site.register(InterviewExperience)