import logging
from pathlib import Path
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.views import View
from django.utils.encoding import smart_str
from django.shortcuts import render


from .models import Resume, Template, ResumeCustomization
from .serializers import ResumeSerializer, TemplateSerializer
from .utils import get_client_ip, is_ip_in_range, SchemaLoader


# Configuración del logger
logger = logging.getLogger(__name__)


@extend_schema(tags=["Resumes"])
@extend_schema_view(
    get=extend_schema(summary="Obtener un resume", responses={200: ResumeSerializer}),
    put=extend_schema(
        summary="Actualizacion de reemplazo del resume", request=ResumeSerializer
    ),
    patch=extend_schema(
        summary="Actualización parcial del resume",
        request=ResumeSerializer,
        responses={200: ResumeSerializer},
        examples=[
            OpenApiExample(
                "Actualización parcial del resumen.",
                summary="Ejemplo de datos parciales",
                value={
                    "name": "nuevo nombre",
                    "summary": "nuevo summary",
                    "skills": [
                        {
                            "id": 1,
                            "name": "actualiza el skill",
                            "level": "Master",
                            "keywords": ["HTML", "CSS", "JavaScript"],
                        }
                    ],
                },
                request_only=True,
            )
        ],
    ),
    delete=extend_schema(
        summary="Eliminar un resume",
    ),
)
class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_queryset(self):
        return Resume.get_with_customization(self.request.user)

    def get_object(self):
        """Sobreescribe get_object para asegurarse de que customization esté presente"""
        obj = super().get_object()
        obj.customization = next(iter(obj.customization_list), None)
        return obj


@extend_schema(tags=["Resumes"])
@extend_schema_view(
    get=extend_schema(
        summary="Listar todos los resumes",
        description="Retorna una lista todos los resumes del usuario.",
    ),
    post=extend_schema(
        summary="Crear un nuevo resume",
        description="Crea un nuevo resume con los datos proporcionados y devuelve el objeto creado.",
        request=ResumeSerializer,
        responses={201: ResumeSerializer},
        examples=[
            OpenApiExample(
                "Ejemplo de creación de resume",
                summary="Ejemplo de datos para crear un resume",
                value={
                    "skills": [
                        {
                            "name": "Web Development",
                            "level": "Master",
                            "keywords": ["HTML", "CSS", "JavaScript"],
                        }
                    ],
                    "experiences": [
                        {
                            "name": "Desarrollador Web",
                            "position": "Full Stack Developer",
                            "url": "https://company.com",
                            "summary": "Parte del equipo de desarrollo.",
                        }
                    ],
                    "full_name": "Leonardo",
                    "email": "3X6Tt@example.com",
                    "summary": "Desarrollador web con experiencia...",
                    "template_selected": 1,
                },
                request_only=True,
            )
        ],
    ),
)
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Solo retorna los currículos del usuario.
        return Resume.get_with_customization(self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario al crear un resume
        serializer.save(user=self.request.user)


@extend_schema(tags=["Templates"])
@extend_schema_view(
    get=extend_schema(
        summary="Listar todos los templates",
        description="Retorna una lista todos los templates.",
        responses={200: TemplateSerializer(many=True)},
    ),
    post=extend_schema(
        summary="Crear un nuevo template",
        description="Crea un nuevo template con los datos proporcionados y devuelve el objeto creado.",
        request=TemplateSerializer,
        responses={200: TemplateSerializer},
        examples=[
            OpenApiExample(
                "Ejemplo de creación de template",
                description="Ejemplo de datos para crear un template",
                value={
                    "name": "Nuevo Template",
                    "componet_name": "mi-componente",
                    "customization_rules": {
                        "color": ["red", "blue", "green"],
                        "margins": {"min": 0, "max": 64},
                        "font_size": {"min": 0, "max": 64},
                    },
                    "descripcion": "Descripción del template",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Schema de reglas de personalización",
                value=SchemaLoader.load_schema("customization_rules.json"),
                description="Esquema de reglas de personalización que se utiliza para validar los datos de personalización especificados en el campo ´customization_rules´.",
                request_only=True,
            ),
        ],
    ),
)
class TemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def patch(self, request, *args, **kwargs):
    #     logger.info(
    #         f"Intentando actualizar el template para el resume: {request.data.get('resume_id')}"
    #     )
    #     try:
    #         resume_id = request.data.get("resume_id")
    #         template_selected = request.data.get("template_selected")

    #         if not resume_id or not template_selected:
    #             logger.warning("Faltan resume_id o template_selected en la solicitud")
    #             return Response(
    #                 {"error": "resume_id y template_selected son requeridos"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    #         template = get_object_or_404(Template, id=template_selected)

    #         resume.template_selected = template
    #         resume.save()
    #         logger.info(
    #             f"Template actualizado exitosamente para el resume: {resume_id}"
    #         )
    #         return Response(
    #             {"success": "Resume updated successfully"},
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as e:
    #         logger.error(f"Error al actualizar el template: {str(e)}")
    #         raise


@extend_schema(tags=["Templates"])
@extend_schema_view(
    get=extend_schema(
        summary="Obtener un template",
        description="Retorna un template con el id proporcionado.",
    ),
    put=extend_schema(
        summary="Actualización de reemplazo del template",
        request=TemplateSerializer,
    ),
    patch=extend_schema(
        summary="Actualización de reemplazo del template",
        request=TemplateSerializer,
    ),
    delete=extend_schema(
        summary="Eliminación del template",
        description="Elimina el template con el id proporcionado.",
    ),
)
class TemplateDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        logger.info("Intentando refrescar el token")
        try:
            # Obtener el refresh token de la solicitud
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.warning("Refresh token no proporcionado")
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
                logger.warning("Token no válido: posible acceso no autorizado")
                token.blacklist()
                raise TokenError("Token no válido: posible acceso no autorizado")

            access_token = str(token.access_token)
            logger.info("Token refrescado exitosamente")
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.error(f"Error al refrescar el token: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogView(View):
    """
    Vista para visualizar y descargar los logs.
    """

    log_file_path = Path(settings.BASE_DIR) / "logs_del_sistema.log"

    def get(csl, request, *args, **kwargs):
        if not csl.log_file_path.exists():
            raise Http404("El archivo de logs no existe.")

        logs = csl.log_file_path.read_text()
        lines = logs.split("\n")
        last_logs = lines[::-1][:50][::-1]

        if "download" in request.GET:
            response = HttpResponse(logs, content_type="text/plain")
            response["Content-Disposition"] = (
                f'attachment; filename="{smart_str(csl.log_file_path.name)}"'
            )
            return response

        return render(request, "resume_app/logs.html", {"logs": "\n".join(last_logs)})
