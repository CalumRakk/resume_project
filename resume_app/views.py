from rest_framework import generics
from .models import Resume
from .serializers import ResumeSerializer


class ResumeDetailDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = "id"


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
