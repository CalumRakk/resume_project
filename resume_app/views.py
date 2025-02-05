from rest_framework import generics, status
from .models import Resume, Template
from .serializers import ResumeSerializer, TemplateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Solo retorna los currículos del usuario autenticado
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado al crear un resume
        serializer.save(user=self.request.user)


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
                # Verifica que el resume pertenece al usuario autenticado
                resume = Resume.objects.get(id=resume_id, user=request.user)
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
