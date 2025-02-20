import logging
from pathlib import Path
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.views import View
from django.utils.encoding import smart_str
from django.shortcuts import render


from .models import Resume, Template, ResumeCustomization
from .serializers import ResumeSerializer, TemplateSerializer
from .utils import get_client_ip, is_ip_in_range


# Configuración del logger
logger = logging.getLogger(__name__)


@extend_schema(tags=["Resumes"])
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

    @extend_schema(
        summary="Obtener un resume",
        description="Retorna un resume del usuario.",
        responses={200: ResumeSerializer},
    )
    def get(self, request, *args, **kwargs):
        logger.info(
            f"Intentando obtener el resume con ID: {kwargs.get('id')} para el usuario: {request.user}"
        )
        try:
            response = super().get(request, *args, **kwargs)
            logger.info(f"Resume obtenido exitosamente: {kwargs.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Error al obtener el resume: {str(e)}")
            raise

    @extend_schema(
        summary="Actualizacion de reemplazo del resume",
        description="Actualización de reemplazo de un Resumen completo en la base de datos. Reemplaza por completo los datos existentes con los nuevos datos proporcionados y recibe como respuesta el objeto completo actualizado.",
        request=ResumeSerializer,
        responses={200: ResumeSerializer},
    )
    def put(self, request, *args, **kwargs):
        logger.info(
            f"Intentando reemplazar el resume con ID: {kwargs.get('id')} para el usuario: {request.user}"
        )
        try:
            response = super().put(request, *args, **kwargs)
            logger.info(f"Resume actualizado exitosamente: {kwargs.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Error al actualizar el resume: {str(e)}")
            raise

    @extend_schema(
        summary="Eliminar el resumen",
        description="Elimina el resumen especificado en la url.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        logger.info(
            f"Intentando eliminar el resume con ID: {kwargs.get('id')} para el usuario: {request.user}"
        )
        try:
            response = super().delete(request, *args, **kwargs)
            logger.info(f"Resume eliminado exitosamente: {kwargs.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Error al eliminar el resume: {str(e)}")
            raise

    @extend_schema(
        summary="Actualización parcial del resumen",
        description="Actualización parcial del resumen. Sólo se actualizan los campos proporcionados y recibe como respuesta el objeto completo actualizado.",
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
                            "level": "Avanzado",
                            "orden": 0,
                        },
                        {"name": "crea un nuevo skill", "level": "Experto", "orden": 1},
                    ],
                },
                request_only=True,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        logger.info(
            f"Intentando actualizar el template para el resume: {kwargs.get('id')}"
        )
        try:
            response = super().patch(request, *args, **kwargs)
            logger.info(
                f"Template actualizado exitosamente para el resume: {kwargs.get('id')}"
            )
            return response
        except Exception as e:
            logger.error(f"Error al actualizar el template: {str(e)}")
            raise


@extend_schema(tags=["Resumes"])
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Solo retorna los currículos del usuario.
        return Resume.get_with_customization(self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario al crear un resume
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Listar todos los resumes",
        description="Retorna una lista todos los resumes del usuario.",
        responses={200: ResumeSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        logger.info(f"Listando resumes para el usuario: {request.user}")
        try:
            response = super().get(request, *args, **kwargs)
            logger.info(
                f"Resumes listados exitosamente para el usuario: {request.user}"
            )
            return response
        except Exception as e:
            logger.error(f"Error al listar resumes: {str(e)}")
            raise

    @extend_schema(
        summary="Crear un nuevo resume",
        description="Crea un nuevo resume en la base de datos y retorna el objeto creado.",
        request=ResumeSerializer,
        responses={201: ResumeSerializer},
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Intentando crear un nuevo resume para el usuario: {request.user}")
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Resume creado exitosamente para el usuario: {request.user}")
            return response
        except Exception as e:
            logger.error(f"Error al crear el resume: {str(e)}")
            raise


@extend_schema(tags=["Templates"])
class TemplateListResumeTemplateUpdateView(APIView):
    @extend_schema(
        summary="Listar todos los templates",
        description="Retorna una lista todos los templates.",
        responses={200: TemplateSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        logger.info("Listando todos los templates")
        try:
            templates = Template.objects.all()
            serializer = TemplateSerializer(templates, many=True)
            logger.info("Templates listados exitosamente")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error al listar templates: {str(e)}")
            raise

    @extend_schema(
        summary="Actualizar un template",
        description="Actualiza el template de un resumen especifico del usuario.",
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
        logger.info(
            f"Intentando actualizar el template para el resume: {request.data.get('resume_id')}"
        )
        try:
            resume_id = request.data.get("resume_id")
            template_selected = request.data.get("template_selected")

            if not resume_id or not template_selected:
                logger.warning("Faltan resume_id o template_selected en la solicitud")
                return Response(
                    {"error": "resume_id y template_selected son requeridos"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            template = get_object_or_404(Template, id=template_selected)

            resume.template_selected = template
            resume.save()
            logger.info(
                f"Template actualizado exitosamente para el resume: {resume_id}"
            )
            return Response(
                {"success": "Resume updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error al actualizar el template: {str(e)}")
            raise


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
