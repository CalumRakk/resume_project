from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.id}"


class Resume(BaseModel):
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True)
    template_selected = models.ForeignKey(
        "Template", on_delete=models.CASCADE, related_name="resumes", null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )


class Skill(BaseModel):
    name = models.CharField(max_length=100, default="Web Development")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    orden = models.PositiveIntegerField()
    keywords = models.JSONField(default=list, null=True)
    level = models.CharField(default="Master", max_length=100, null=True)

    class Meta:
        ordering = ["orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["resume", "orden"], name="unique_order_per_resume_skill"
            )
        ]


class Experience(BaseModel):
    name = models.CharField(max_length=100, default="Company Name")
    position = models.CharField(max_length=100, default="President")
    start_date = models.DateField()
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="experiences"
    )
    orden = models.PositiveIntegerField()
    url = models.URLField(default="https://company.com", null=True)
    summary = models.TextField(default="Description…", null=True)
    highlights = models.JSONField(default=list, null=True)
    end_date = models.DateField(null=True)

    class Meta:
        ordering = ["orden"]
        constraints = [
            # Garantiza que dos experiencias asociadas al mismo Resume no tengan el mismo orden.
            models.UniqueConstraint(
                fields=["resume", "orden"], name="unique_order_per_resume_experience"
            )
        ]


class Template(BaseModel):
    name = models.CharField(max_length=100)
    componet_name = models.CharField(max_length=100)
    customazation_rules = models.JSONField(default=list)
    descripcion = models.TextField(null=True)


class ResumeTemplate(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)


class ResumeCustomization(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)
