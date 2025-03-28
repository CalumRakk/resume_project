import logging
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import smart_str
from django.views import View
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from .models import Resume, ResumeCustomization, Template
from .serializers import ResumeSerializer, TemplateSerializer
from .utils import SchemaLoader, get_client_ip, is_ip_in_range

# Logger configuration
logger = logging.getLogger(__name__)


@extend_schema(tags=["Resumes"])
@extend_schema_view(
    get=extend_schema(summary="Get a resume", responses={200: ResumeSerializer}),
    put=extend_schema(
        summary="Replacement update of the resume", request=ResumeSerializer
    ),
    patch=extend_schema(
        summary="Partial update of the resume",
        request=ResumeSerializer,
        responses={200: ResumeSerializer},
        examples=[
            OpenApiExample(
                "Partial resume update.",
                summary="Example of partial data",
                value={
                    "name": "new name",
                    "summary": "new summary",
                    "skills": [
                        {
                            "id": 1,
                            "name": "update the skill",
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
        summary="Delete a resume",
    ),
)
class ResumeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_queryset(self):
        return Resume.get_with_customization(self.request.user)

    def get_object(self):
        """Overrides get_object to ensure customization is present"""
        obj = super().get_object()
        obj.customization = next(iter(obj.customization_list), None)
        return obj


@extend_schema(tags=["Resumes"])
@extend_schema_view(
    get=extend_schema(
        summary="List all resumes",
        description="Returns a list of all user's resumes.",
    ),
    post=extend_schema(
        summary="Create a new resume",
        description="Creates a new resume with the provided data and returns the created object.",
        request=ResumeSerializer,
        responses={201: ResumeSerializer},
        examples=[
            OpenApiExample(
                "Resume creation example",
                summary="Example of data to create a resume",
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
                            "name": "Web Developer",
                            "position": "Full Stack Developer",
                            "url": "https://company.com",
                            "summary": "Part of the development team.",
                            "start_date": "2022-01-01",
                        }
                    ],
                    "full_name": "Leonardo",
                    "email": "3X6Tt@example.com",
                    "summary": "Web developer with experience...",
                    "template_selected": 2,
                },
                request_only=True,
            )
        ],
    ),
)
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Only returns the user's resumes.
        return Resume.get_with_customization(self.request.user)

    def perform_create(self, serializer):
        # Automatically assigns the user when creating a resume
        serializer.save(user=self.request.user)


@extend_schema(tags=["Templates"])
@extend_schema_view(
    get=extend_schema(
        summary="List all templates",
        description="Returns a list of all templates.",
        responses={200: TemplateSerializer(many=True)},
    ),
    post=extend_schema(
        summary="Create a new template",
        description="Creates a new template with the provided data and returns the created object.",
        request=TemplateSerializer,
        responses={200: TemplateSerializer},
        examples=[
            OpenApiExample(
                "Template creation example",
                description="Example of data to create a template",
                value={
                    "name": "New Template",
                    "componet_name": "my-component",
                    "customization_rules": {
                        "color": ["red", "blue", "green"],
                        "margins": {"min": 0, "max": 64},
                        "font_size": {"min": 0, "max": 64},
                    },
                    "descripcion": "Template description",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Customization rules schema",
                value=SchemaLoader.load_schema("customization_rules.json"),
                description="Customization rules schema used to validate the customization data specified in the ´customization_rules´ field.",
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
    #         f"Attempting to update the template for the resume: {request.data.get('resume_id')}"
    #     )
    #     try:
    #         resume_id = request.data.get("resume_id")
    #         template_selected = request.data.get("template_selected")

    #         if not resume_id or not template_selected:
    #             logger.warning("Missing resume_id or template_selected in the request")
    #             return Response(
    #                 {"error": "resume_id and template_selected are required"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    #         template = get_object_or_404(Template, id=template_selected)

    #         resume.template_selected = template
    #         resume.save()
    #         logger.info(
    #             f"Template updated successfully for the resume: {resume_id}"
    #         )
    #         return Response(
    #             {"success": "Resume updated successfully"},
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as e:
    #         logger.error(f"Error updating the template: {str(e)}")
    #         raise


@extend_schema(tags=["Templates"])
@extend_schema_view(
    get=extend_schema(
        summary="Get a template",
        description="Returns a template with the provided id.",
    ),
    put=extend_schema(
        summary="Replacement update of the template",
        request=TemplateSerializer,
    ),
    patch=extend_schema(
        summary="Replacement update of the template",
        request=TemplateSerializer,
    ),
    delete=extend_schema(
        summary="Template deletion",
        description="Deletes the template with the provided id.",
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
        logger.info("Attempting to refresh the token")
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.warning("Refresh token not provided")
                raise TokenError("Refresh token not provided")

            token = RefreshToken(refresh_token)
            user_metadata = token.payload.get("user_metadata", {})
            stored_ip = user_metadata.get("ip_address")
            stored_user_agent = user_metadata.get("user_agent")
            current_ip = get_client_ip(request)
            current_user_agent = request.META.get("HTTP_USER_AGENT", "")

            if stored_user_agent != current_user_agent or not is_ip_in_range(
                current_ip, stored_ip
            ):
                logger.warning("Invalid token: possible unauthorized access")
                token.blacklist()
                raise TokenError("Invalid token: possible unauthorized access")

            access_token = str(token.access_token)
            logger.info("Token refreshed successfully")
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.error(f"Error refreshing the token: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogView(View):
    """
    View to visualize and download logs.
    """

    log_file_path = Path(settings.BASE_DIR) / "logs_del_sistema.log"

    def get(csl, request, *args, **kwargs):
        if not csl.log_file_path.exists():
            raise Http404("The log file does not exist.")

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
