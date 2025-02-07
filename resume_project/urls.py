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
from rest_framework_simplejwt.views import TokenObtainPairView
from resume_app.views import (
    ResumeDetailUpdateDestroyView,
    ResumeListCreateView,
    TemplateListResumeTemplateUpdateView,
    CustomTokenRefreshView,
    LogView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "v1/",
        include(
            [
                path(
                    "resumes/<int:id>/",
                    ResumeDetailUpdateDestroyView.as_view(),
                    name="resume-detail-destroy",
                ),
                path(
                    "resumes/",
                    ResumeListCreateView.as_view(),
                    name="resume-list-create",
                ),
                path(
                    "templates/",
                    TemplateListResumeTemplateUpdateView.as_view(),
                    name="template-list-resume-template-update",
                ),
                path("login/", TokenObtainPairView.as_view(), name="login"),
                path(
                    "refresh-token/",
                    CustomTokenRefreshView.as_view(),
                    name="refresh_token",
                ),
                # path("logout/", LogoutView.as_view(), name="logout"),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("logs/", LogView.as_view(), name="view_logs"),
    ]
    urlpatterns += [
        path(
            "v1/",
            include(
                [
                    path("schema/", SpectacularAPIView.as_view(), name="schema"),
                    path(
                        "swagger/",
                        SpectacularSwaggerView.as_view(url_name="schema"),
                        name="swagger-ui",
                    ),
                ]
            ),
        )
    ]
