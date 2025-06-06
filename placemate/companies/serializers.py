from rest_framework import serializers
from .models import TechStack, Company, Role, InterviewExperience, Review

#TechStack Serializer
class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ["id", "name"]


#Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    tech_stack_ids = serializers.PrimaryKeyRelatedField(
        queryset=TechStack.objects.all(), many=True, write_only=True, source='tech_stack'
    )

    class Meta:
        model = Role
        fields = [
            "id", "company", "title", "description", "tech_stack", "tech_stack_ids",
            "average_ctc", "job_location", "openings_per_year"
        ]


#Interview Experience Serializer
class InterviewExperienceSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), write_only=True, source='company'
    )
    role = serializers.StringRelatedField(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), write_only=True, source='role', allow_null=True, required=False
    )
    tech_stack = TechStackSerializer(many=True, read_only=True)
    tech_stack_ids = serializers.PrimaryKeyRelatedField(
        queryset=TechStack.objects.all(), many=True, write_only=True, source='tech_stack'
    )

    class Meta:
        model = InterviewExperience
        fields = [
            'id', 'company', 'company_id', 'role', 'role_id',
            'experience', 'outcome', 'difficulty',
            'tech_stack', 'tech_stack_ids', 'created_at'
        ]


#Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), write_only=True, source='company'
    )

    class Meta:
        model = Review
        fields = [
            "id", "company", "company_id", "reviewer_name", "rating",
            "pros", "cons", "work_life_balance", "culture", "created_at"
        ]


#Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    tech_stack_ids = serializers.PrimaryKeyRelatedField(
        queryset=TechStack.objects.all(), many=True, write_only=True, source='tech_stack'
    )

    # Nested
    roles = RoleSerializer(many=True, read_only=True)
    interview_experiences = InterviewExperienceSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            "id", "name", "slug", "description", "tech_stack", "tech_stack_ids",
            "headquarters", "founded_year", "employee_count", "industry", "website", "average_ctc",
            "roles", "interview_experiences", "reviews"
        ]
