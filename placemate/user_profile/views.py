from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset= UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
