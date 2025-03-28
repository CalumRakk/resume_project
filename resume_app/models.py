from django.db import models
from django.conf import settings
from resume_app.utils import check_list_does_not_exceed_50, is_valid_webcomponent
from django.db.models import Prefetch, F


class BaseModel(models.Model):
    """
    Abstract base model that provides the `created_at` and `updated_at` columns
    to record creation and modification dates of the records.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date the record was last modified."
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.__class__.__name__}] {getattr(self, 'name', '')} {self.id}"


class Resume(BaseModel):
    """
    Model that represents a resume.
    """

    full_name = models.CharField(
        max_length=100, null=True, help_text="Full name of the user."
    )
    email = models.EmailField(
        null=True, help_text="Email address associated with the resume."
    )
    summary = models.TextField(
        null=True,
        help_text="Summary or general description of the user.",
        max_length=500,
    )
    template_selected = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        related_name="resumes",
        null=True,
        help_text="Template selected for the display of the resume.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
        help_text="User owning the resume.",
    )

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"

    @classmethod
    def get_with_customization(cls, user):
        """
        Gets the list of the user's resumes, prefetching the
        customization (`ResumeCustomization`) associated with each resume.

        - Uses `select_related("template_selected")` to avoid extra queries
        when accessing the relationship with `Template`.
        - Uses `prefetch_related` with `Prefetch` to load the customizations
        (`ResumeCustomization`) that match the selected template for each resume.
        - Converts `customization_list` to a single `customization` object to
        facilitate direct access in the views.

        Returns:
            QuerySet: List of `Resume` objects, each with its `customization` preloaded.
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
    Represents a skill within the resume.
    """

    name = models.CharField(
        max_length=100, default="Web Development", help_text="Name of the skill."
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="Resume to which the skill belongs.",
    )
    keywords = models.JSONField(
        default=list,
        null=True,
        help_text="Keywords associated with the skill.",
        validators=[check_list_does_not_exceed_50],
    )
    level = models.CharField(
        default="Master",
        max_length=100,
        null=True,
        help_text="Skill level (e.g., Basic, Advanced, Expert).",
    )

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Experience(BaseModel):
    """
    Represents a work experience within the resume.
    """

    name = models.CharField(
        max_length=100,
        default="Company Name",
        help_text="Name of the company or organization.",
    )
    position = models.CharField(
        max_length=100,
        default="President",
        help_text="Position held in the company.",
    )
    start_date = models.DateField(help_text="Employment start date.")
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="experiences",
        help_text="Resume to which the experience belongs.",
    )
    url = models.URLField(
        default="https://company.com",
        null=True,
        help_text="Link to the company",
        max_length=100,
    )
    summary = models.TextField(
        default="Description…",
        null=True,
        help_text="General description of the work experience.",
        max_length=500,
    )
    highlights = models.JSONField(
        default=list,
        null=True,
        help_text="List of highlights of the job.",
        validators=[check_list_does_not_exceed_50],
    )
    end_date = models.DateField(
        null=True,
        help_text="Employment end date. NULL if still in progress.",
    )

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"


class Template(BaseModel):
    """
    Represents a design template for resumes.
    """

    name = models.CharField(max_length=100, help_text="Name of the template.")
    componet_name = models.CharField(
        max_length=100,
        help_text="Name of the web component associated with the template.",
        validators=[is_valid_webcomponent],
    )
    customization_rules = models.JSONField(
        default=dict, help_text="Template customization rules."
    )
    descripcion = models.TextField(
        null=True, help_text="Description of the template.", max_length=500
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="templates",
        help_text="User creating the template.",
    )

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"


class ResumeCustomization(BaseModel):
    """
    Represents a customization applied to a resume with a specific template.
    """

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        help_text="Resume to which the customization is applied.",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        help_text="Template selected for customization.",
    )
    custom_styles = models.JSONField(
        default=dict, help_text="Custom styles applied to the resume."
    )

    class Meta:
        verbose_name = "Resume Customization"
        verbose_name_plural = "Resume Customizations"
        constraints = [
            models.UniqueConstraint(
                fields=["resume", "template"],
                name="unique_resume_template_customization",
            )
        ]
