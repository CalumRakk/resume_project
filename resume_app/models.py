from django.db import models


class Resume(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField()
    template_selected = models.ForeignKey(
        "Template", on_delete=models.CASCADE, related_name="resumes", null=True
    )

    def __str__(self):
        return f"[Resume] {self.full_name}"


class Skill(models.Model):
    name = models.CharField(max_length=100, default="Web Development")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    level = models.CharField(default="Master", max_length=100)
    keywords = models.JSONField(default=list)
    orden = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["resume", "orden"], name="unique_order_per_resume_skill"
            )
        ]


class Experience(models.Model):
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
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        constraints = [
            # Garantiza que dos experiencias asociadas al mismo Resume no tengan el mismo orden.
            models.UniqueConstraint(
                fields=["resume", "orden"], name="unique_order_per_resume_experience"
            )
        ]

    def __str__(self):
        return f"[Experience] {self.name}"


class Template(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.TextField()
    componet_name = models.CharField(max_length=100)
    customazation_rules = models.JSONField(default=list)

    def __str__(self):
        return f"[Template] {self.name}"


class ResumeTemplate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)


class ResumeCustomization(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    custom_styles = models.JSONField(default=list)
