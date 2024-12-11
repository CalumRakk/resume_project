from django.db import models


class Resume(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField()

    def __str__(self):
        return f"[Resume] {self.full_name}"


class Skill(models.Model):
    name = models.CharField(max_length=100, default="Web Development")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    level = models.CharField(default="Master", max_length=100)
    keywords = models.JSONField(default=list)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"[Experience] {self.name}"


class Template(models.Model):
    name = models.CharField(max_length=100)
    html_structure = models.TextField()  # Aquí guardamos el diseño en HTML.
    styles = models.JSONField(default=dict)  # Reglas CSS dinámicas.
    resume = models.OneToOneField(
        Resume, on_delete=models.CASCADE, related_name="template"
    )

    def __str__(self):
        return f"[Template] {self.name}"
