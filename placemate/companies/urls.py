from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'techstack', views.TechStackViewSet)
router.register(r'interview-experience', views.InterviewExperienceViewSet)
router.register(r'company-reviews', views.ReviewViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('fetch-company-info/', views.fetch_and_store_company_info, name='fetch_company_info'),
]
