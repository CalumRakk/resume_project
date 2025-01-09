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
from django.urls import path, include
from resume_app import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"resumes", views.ResumeViewSet)
router.register(r"skills", views.SkillViewSet)
router.register(r"experiences", views.ExperienceViewSet)
router.register(r"templates", views.TemplateViewSet)
router.register(r"customizations", views.ResumeCustomizationViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/resume/<int:resume_id>/", views.ResumeAPIView.as_view(), name="resume-api"
    ),
    path("resume/<int:resume_id>/", views.serve_resume_page, name="resume-page"),
    path("api/", include(router.urls)),
    path("<int:resume_id>/", views.index, name="index"),
    path("__reload__/", include("django_browser_reload.urls")),
]
