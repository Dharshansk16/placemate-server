from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company, Role, TechStack, InterviewExperience, Review
from .serializers import (
    CompanySerializer,
    RoleSerializer,
    TechStackSerializer,
    InterviewExperienceSerializer,
    ReviewSerializer
)
from .gemini import fetch_company_data
import json
import datetime


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.prefetch_related('tech_stack', 'roles').all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related('company').prefetch_related('tech_stack').all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [IsAuthenticated]


class InterviewExperienceViewSet(viewsets.ModelViewSet):
    queryset = InterviewExperience.objects.select_related('company', 'role').prefetch_related('tech_stack').all()
    serializer_class = InterviewExperienceSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('company').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_company_info(request):
    company_name = request.query_params.get("company_name")
    if not company_name:
        return Response({"error": "Company name is required."}, status=400)

    company = Company.objects.filter(name__iexact=company_name).first()
    if not company:
        return Response({"error": "Company not found."}, status=404)

    serializer = CompanySerializer(company)
    return Response(serializer.data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fetch_and_store_company_info(request):
    company_name = request.data.get("company_name")
    if not company_name:
        return Response({"error": "Company name is required."}, status=400)

    # Check for recent updates
    company = Company.objects.filter(name__iexact=company_name).first()
    is_fresh= company and company.last_updated > timezone.now() - datetime.timedelta(days=30)

        
    if is_fresh:
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    # Fetch data from Gemini
    raw_json = fetch_company_data(company_name)
    try:
        json_data = raw_json[raw_json.find('{'):raw_json.rfind('}')+1]
        data = json.loads(json_data)
    except json.JSONDecodeError:
        return Response({"error": "Failed to decode JSON from Gemini."}, status=500)

    # Create or update company
    company, _ = Company.objects.get_or_create(name=data["name"])
    company.description = data.get("description", "")
    company.headquarters = data.get("headquarters")
    company.founded_year = data.get("founded_year")
    company.employee_count = data.get("employee_count")
    company.industry = data.get("industry")
    company.website = data.get("website")
    company.average_ctc = data.get("average_ctc")
    company.last_updated = timezone.now()
    company.save()

    # General Tech Stack
    tech_objs = []
    for tech in data.get("tech_stack", []):
        tech_obj, _ = TechStack.objects.get_or_create(name=tech)
        tech_objs.append(tech_obj)
    company.tech_stack.set(tech_objs)

    # Roles
    for role_data in data.get("roles", []):
        role_obj, _ = Role.objects.get_or_create(company=company, title=role_data["title"])
        role_obj.description = role_data.get("description", "")
        role_obj.average_ctc = role_data.get("average_ctc")
        role_obj.job_location = role_data.get("job_location")
        role_obj.openings_per_year = role_data.get("openings_per_year")
        role_obj.save()

        role_techs = []
        for tech in role_data.get("tech_stack", []):
            tech_obj, _ = TechStack.objects.get_or_create(name=tech)
            role_techs.append(tech_obj)
        role_obj.tech_stack.set(role_techs)

    # Interview Experiences
    for experience in data.get("interview_experiences", []):
        role = Role.objects.filter(company=company, title=experience.get("role_title")).first()
        if not role:
            continue
        exp_obj = InterviewExperience.objects.create(
            company=company,
            role=role,
            experience=experience.get("experience", ""),
            outcome=experience.get("outcome", ""),
            difficulty=experience.get("difficulty", "")
        )
        exp_techs = []
        for tech in experience.get("tech_stack", []):
            tech_obj, _ = TechStack.objects.get_or_create(name=tech)
            exp_techs.append(tech_obj)
        exp_obj.tech_stack.set(exp_techs)

    # Reviews
    for review in data.get("reviews", []):
        Review.objects.create(
            company=company,
            reviewer_name=review.get("reviewer_name", ""),
            rating=review.get("rating", 0),
            review_text=review.get("review_text", ""),
            pros=review.get("pros", ""),
            cons=review.get("cons", ""),
            work_life_balance=review.get("work_life_balance", 0),
            culture=review.get("culture", 0),
        )

    serializer= CompanySerializer(company)
    return Response(serializer.data, status=200)

