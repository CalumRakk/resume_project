from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.id}"


class Resume(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField()
    template_selected = models.ForeignKey(
        "Template", on_delete=models.CASCADE, related_name="resumes", null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )


class Skill(BaseModel):
    name = models.CharField(max_length=100, default="Web Development")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    level = models.CharField(default="Master", max_length=100)
    keywords = models.JSONField(default=list)
    orden = models.PositiveIntegerField()

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
    url = models.URLField(default="https://company.com")
    highlights = models.JSONField(default=list)
    summary = models.TextField(default="Description…")
    start_date = models.DateField()
    end_date = models.DateField()
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="experiences"
    )
    orden = models.PositiveIntegerField()

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
    descripcion = models.TextField()
    componet_name = models.CharField(max_length=100)
    customazation_rules = models.JSONField(default=list)


class ResumeTemplate(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)


class ResumeCustomization(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="session")
    token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Sesión de {self.user.username} desde {self.ip_address}"
