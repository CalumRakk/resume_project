"""
URL configuration for resume_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from resume_app.views import (
    ResumeDetailUpdateDestroyView,
    ResumeListCreateView,
    TemplateListResumeTemplateUpdateView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "v1/resumes/<int:id>/",
        ResumeDetailUpdateDestroyView.as_view(),
        name="resume-detail-destroy",
    ),
    path("v1/resumes/", ResumeListCreateView.as_view(), name="resume-list-create"),
    path(
        "v1/templates/",
        TemplateListResumeTemplateUpdateView.as_view(),
        name="template-list-resume-template-update",
    ),
    path("v1/login/", TokenObtainPairView.as_view(), name="login"),
    path("v1/refresh-token/", CustomTokenRefreshView.as_view(), name="refresh_token"),
    # path("logout/", LogoutView.as_view(), name="logout"),
]
