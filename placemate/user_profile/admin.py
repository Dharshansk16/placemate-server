from django.contrib import admin
from .models import UserProfile,Skill,JobInterest

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(JobInterest)