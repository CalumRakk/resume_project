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
            resume = Resume.objects.get(id=request.data.pop("resume_id"))
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
