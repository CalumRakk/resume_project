from rest_framework import viewsets
from django.db.models import Prefetch
import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume, Template, Skill, Experience, ResumeCustomization
from .serializers import (
    TemplateSerializer,
    ResumeSerializer,
    SkillSerializer,
    ExperienceSerializer,
    ResumeCustomizationSerializer,
)
from django.views.decorators.csrf import csrf_exempt

# views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class ResumeAPIView(APIView):
    def get(self, request, resume_id):
        resume = Resume.objects.get(pk=resume_id)
        resume_serializer = ResumeSerializer(resume, context={"request": request})
        resume_data = resume_serializer.data

        template = Template.objects.get(pk=resume.template_selected.pk)
        template_serializer = TemplateSerializer(template, context={"request": request})
        template_data = template_serializer.data
        data = {
            "resume": resume_data,
            "template_selected": template_data,
        }
        return Response(data)


@csrf_exempt
def serve_resume_page(request, resume_id):

    if request.method == "POST":
        data = json.loads(request.body)
        resume = Resume.objects.get(pk=resume_id)
        resume.full_name = data["full_name"]
        resume.email = data["email"]
        resume.summary = data["summary"]
        resume.save()
        return Response(status=status.HTTP_200_OK)

    resume = Resume.objects.get(pk=resume_id)
    resume_serializer = ResumeSerializer(resume, context={"request": request})
    resume_data = resume_serializer.data

    template = Template.objects.get(pk=resume.template_selected.pk)
    template_serializer = TemplateSerializer(template, context={"request": request})
    template_data = template_serializer.data
    data = {
        "resume": resume_data,
        "template_selected": template_data,
    }
    json_data = json.dumps(data)
    return render(request, "resume_app/resume.html", context={"user_resume": json_data})


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


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class ResumeCustomizationViewSet(viewsets.ModelViewSet):
    queryset = ResumeCustomization.objects.all()
    serializer_class = ResumeCustomizationSerializer


# Create your views here.
@api_view(["GET"])
def index(request, resume_id):

    return render(request, "resume_app/index.html", {"resume_id": resume_id})
