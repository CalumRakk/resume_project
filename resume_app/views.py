from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404

from .utils import get_client_ip
from .middleware import is_ip_in_range
from .models import Resume, Template
from .serializers import ResumeSerializer, TemplateSerializer


@extend_schema(tags=["Resumes"])
class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Obtener un resume",
        description="Retorna un resume del usuario..",
        responses={200: ResumeSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizacion de reemplazo de un resume",
        description="Actualiza un Resumen completo en la base de datos. Reemplaza por completo los datos existentes con los nuevos datos proporcionados.",
        request=ResumeSerializer,
        responses={200: ResumeSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar el resumen",
        description="Elimina el resumen especificado en la url.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema(tags=["Resumes"])
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Solo retorna los currículos del usuario.
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario. al crear un resume
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Listar todos los resumes",
        description="Retorna una lista todos los resumes del usuario..",
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
    @extend_schema(
        summary="Listar todos los templates",
        description="Retorna una lista todos los templates.",
        responses={200: TemplateSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Actualizar un template",
        description="Actualiza el template de un resumen especifico del usuario..",
        request=ResumeSerializer,
        responses={200: ResumeSerializer},
        examples=[
            OpenApiExample(
                "Ejemplo de actualización de template",
                summary="Ejemplo de datos correctos",
                description="Este es un ejemplo de cómo debería verse una solicitud exitosa.",
                value={
                    "resume_id": 1,
                    "template_selected": 2,
                },
                request_only=True,
            )
        ],
    )
    def patch(self, request, *args, **kwargs):
        resume_id = request.data.get("resume_id")
        template_selected = request.data.get("template_selected")

        if not resume_id or not template_selected:
            return Response(
                {"error": "resume_id y template_selected son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        template = get_object_or_404(Template, id=template_selected)

        resume.template_selected = template
        resume.save()
        return Response(
            {"success": "Resume updated successfully"},
            status=status.HTTP_200_OK,
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
            current_ip = get_client_ip(request)
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
