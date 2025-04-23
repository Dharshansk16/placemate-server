from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'techstack', views.TechStackViewSet)
router.register(r'interview-experience', views.InterviewExperienceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]