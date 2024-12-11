from rest_framework import viewsets
from .models import Resume, Template, Skill, Experience
from .serializers import (
    TemplateSerializer,
    ResumeSerializer,
    SkillSerializer,
    ExperienceSerializer,
)


class ResumeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
