from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .middleware import is_ip_in_range
from .models import Resume, Template
from .serializers import ResumeSerializer, TemplateSerializer


@extend_schema(tags=["Resumes"])
class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


@extend_schema(tags=["Resumes"])
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Solo retorna los currículos del usuario autenticado
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado al crear un resume
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Listar todos los resumes",
        description="Retorna una lista todos los resumes del usuario autenticado.",
        responses={200: ResumeSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Crear un nuevo resume",
        description="Crea un nuevo resume en la base de datos y retorna el objeto creado.",
        request=ResumeSerializer,
        responses={201: ResumeSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["Templates"])
class TemplateListResumeTemplateUpdateView(APIView):

    def get(self, request, *args, **kwargs):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
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


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el refresh token de la solicitud
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                raise TokenError("Refresh token no proporcionado")

            token = RefreshToken(refresh_token)
            user_metadata = token.payload.get("user_metadata", {})
            stored_ip = user_metadata.get("ip_address")
            stored_user_agent = user_metadata.get("user_agent")
            current_ip = self._get_client_ip(request)
            current_user_agent = request.META.get("HTTP_USER_AGENT", "")

            if stored_user_agent != current_user_agent or not is_ip_in_range(
                current_ip, stored_ip
            ):
                token.blacklist()
                raise TokenError("Token no válido: posible acceso no autorizado")

            access_token = str(token.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
