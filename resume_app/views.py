from rest_framework import generics, status
from .models import Resume, Template
from .serializers import ResumeSerializer, TemplateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = "id"


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class TemplateListResumeTemplateUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            resume_id = request.data.pop("resume_id")
            template_selected = request.data.pop("template_selected")
            if resume_id and template_selected:
                resume = Resume.objects.get(id=resume_id)
                template = Template.objects.get(id=template_selected)
                resume.template_selected = template
                resume.save()
                return Response(
                    {"success": "Resume updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "resume_id and template_selected are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND
            )
