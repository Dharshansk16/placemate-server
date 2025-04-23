from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Company, Role, TechStack, InterviewExperience
from .serializers import CompanySerializer, RoleSerializer, TechStackSerializer, InterviewExperienceSerializer
from rest_framework.permissions import IsAuthenticated

class CompanyViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing and editing companies.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing and editing roles associated with a company.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class TechStackViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing and editing tech stacks.
    """
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [IsAuthenticated]


class InterviewExperienceViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing and editing interview experiences.
    """
    queryset = InterviewExperience.objects.all()
    serializer_class = InterviewExperienceSerializer
    permission_classes = [IsAuthenticated]
