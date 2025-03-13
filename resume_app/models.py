from django.db import models
from django.conf import settings
from resume_app.utils import check_list_does_not_exceed_50
from django.db.models import Prefetch, F


class BaseModel(models.Model):
    """
    Modelo base abstracto que proporciona las columnas `created_at` y `updated_at`
    para registrar fechas de creación y modificación de los registros.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Fecha de creación del registro."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Fecha de última modificación del registro."
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.__class__.__name__}] {getattr(self, 'name', '')} {self.id}"


class Resume(BaseModel):
    """
    Modelo que representa un resumen.
    """

    full_name = models.CharField(
        max_length=100, null=True, help_text="Nombre completo del usuario."
    )
    email = models.EmailField(
        null=True, help_text="Correo electrónico asociado al resumen."
    )
    summary = models.TextField(
        null=True,
        help_text="Resumen o descripción general del usuario.",
        max_length=500,
    )
    template_selected = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        related_name="resumes",
        null=True,
        help_text="Plantilla seleccionada para la visualización del resumen.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
        help_text="Usuario dueño del resumen.",
    )

    class Meta:
        verbose_name = "Resumen"
        verbose_name_plural = "Resúmenes"

    @classmethod
    def get_with_customization(cls, user):
        """
        Obtiene la lista de resumes del usuario, prefetching la
        personalización (`ResumeCustomization`) asociada con cada resume.

        - Usa `select_related("template_selected")` para evitar consultas extra
        al acceder a la relación con `Template`.
        - Usa `prefetch_related` con `Prefetch` para cargar las personalizaciones
        (`ResumeCustomization`) que coinciden con el template seleccionado de cada resume.
        - Convierte `customization_list` en un solo objeto `customization` para
        facilitar el acceso directo en las vistas.

        Returns:
            QuerySet: Lista de objetos `Resume`, cada uno con su `customization` precargado.
        """
        resumes = (
            Resume.objects.filter(user=user)
            .select_related("template_selected")
            .prefetch_related(
                Prefetch(
                    "resumecustomization_set",
                    queryset=ResumeCustomization.objects.filter(
                        template=F("resume__template_selected")
                    ),
                    to_attr="customization_list",
                )
            )
        )

        for resume in resumes:
            setattr(
                resume, "customization", next(iter(resume.customization_list), None)
            )

        return resumes


class Skill(BaseModel):
    """
    Representa una habilidad dentro del resumen.
    """

    name = models.CharField(
        max_length=100, default="Web Development", help_text="Nombre de la habilidad."
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="Resumen al que pertenece la habilidad.",
    )
    keywords = models.JSONField(
        default=list,
        null=True,
        help_text="Palabras clave asociadas a la habilidad.",
        validators=[check_list_does_not_exceed_50],
    )
    level = models.CharField(
        default="Master",
        max_length=100,
        null=True,
        help_text="Nivel de la habilidad (Ej: Básico, Avanzado, Experto).",
    )

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"


class Experience(BaseModel):
    """
    Representa una experiencia laboral dentro del resumen.
    """

    name = models.CharField(
        max_length=100,
        default="Company Name",
        help_text="Nombre de la empresa u organización.",
    )
    position = models.CharField(
        max_length=100,
        default="President",
        help_text="Puesto desempeñado en la empresa.",
    )
    start_date = models.DateField(help_text="Fecha de inicio del empleo.")
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="experiences",
        help_text="Resumen al que pertenece la experiencia.",
    )
    url = models.URLField(
        default="https://company.com",
        null=True,
        help_text="Enlace a la empresa",
        max_length=100,
    )
    summary = models.TextField(
        default="Description…",
        null=True,
        help_text="Descripción general de la experiencia laboral.",
        max_length=500,
    )
    highlights = models.JSONField(
        default=list,
        null=True,
        help_text="Lista de Aspectos destacados del trabajo.",
        validators=[check_list_does_not_exceed_50],
    )
    end_date = models.DateField(
        null=True,
        help_text="Fecha de finalización del empleo. NULL si aún está en curso.",
    )

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"


class Template(BaseModel):
    """
    Representa una plantilla de diseño para los resúmenes.
    """

    name = models.CharField(max_length=100, help_text="Nombre de la plantilla.")
    componet_name = models.CharField(
        max_length=100, help_text="Nombre del componente web asociado a la plantilla."
    )
    customization_rules = models.JSONField(
        default=list, help_text="Reglas de personalización de la plantilla."
    )
    descripcion = models.TextField(
        null=True, help_text="Descripción de la plantilla.", max_length=500
    )

    class Meta:
        verbose_name = "Plantilla"
        verbose_name_plural = "Plantillas"


class ResumeCustomization(BaseModel):
    """
    Representa una personalización aplicada a un resumen con una plantilla específica.
    """

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        help_text="Resumen al que se aplica la personalización.",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        help_text="Plantilla seleccionada para la personalización.",
    )
    custom_styles = models.JSONField(
        default=list, help_text="Estilos personalizados aplicados al resumen."
    )

    class Meta:
        verbose_name = "Personalización de Resumen"
        verbose_name_plural = "Personalización de Resúmenes"
        constraints = [
            models.UniqueConstraint(
                fields=["resume", "template"],
                name="unique_resume_template_customization",
            )
        ]
