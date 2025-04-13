from django.urls import path, include

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),  # Login,logout, password reset
    path('auth/registration/', include('dj_rest_auth.registration.urls')),#Signup
    path('auth/google/', include('allauth.socialaccount.urls')),  # Google OAuth endpoints
]
