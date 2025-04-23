from rest_framework import serializers
from .models import UserProfile, Skill, JobInterest
from user_auth.models import User

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class JobInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterest
        fields = ['id', 'title']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields= ['id', 'email', 'is_premium', "username"]

class UserProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    job_interests = JobInterestSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'full_name', 'slug', 'created_at', 'updated_at','avatar', 'skills', 'job_interests', 'bio', 'education', 'experience', 'location']
        read_only_fields = ['user','slug', 'created_at', 'updated_at'] 
