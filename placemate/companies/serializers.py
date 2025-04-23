from rest_framework import serializers
from .models import TechStack, Company , Role, InterviewExperience

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model =TechStack
        fields= ["id", "name"]


class CompanySerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    class Meta:
        model=Company
        fields=["id" ,"name","slug", "description", "tech_stack"]


class RoleSerializer(serializers.ModelSerializer):
    tech_stack =TechStackSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields= ["id", "company", "title", "description", "tech_stack"]



class InterviewExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for the InterviewExperience model.
    """
    company = CompanySerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewExperience
        fields = ['id', 'company', 'role', 'experience', 'outcome', 'difficulty', 'tech_stack', 'created_at']

    