from django.core.management.base import BaseCommand
from django.apps import apps


def generate_markdown():
    models = apps.get_models()
    with open("database_schema.md", "w", encoding="utf-8") as f:
        f.write(
            "Documento autogenerado usando el comando `python manage.py generate_markdown`\n\n"
        )
        for model in models:
            if model._meta.verbose_name in [
                "permission",
                "group",
                "user",
                "log entry",
                "content type",
                "session",
                "outstanding token",
                "blacklisted token",
            ]:
                continue
            f.write(f"## {model._meta.verbose_name_plural}\n\n")
            f.write(f"{model.__doc__.strip()}\n\n")
            f.write("| Campo | Tipo | Permite NULL | Descripción |\n")
            f.write("|-------|------|-------------|-------------|\n")
            for field in model._meta.fields:
                null = "✅" if field.null else "❌"
                f.write(
                    f"| {field.name} | {field.get_internal_type()} | {null} | {field.help_text} |\n"
                )
            f.write("\n")


class Command(BaseCommand):
    help = "Genera un archivo Markdown con el esquema de la base de datos"

    def handle(self, *args, **kwargs):
        generate_markdown()
