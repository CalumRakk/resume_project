# Generated by Django 5.1.4 on 2024-12-12 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0003_alter_template_resume"),
    ]

    operations = [
        migrations.RenameField(
            model_name="template",
            old_name="html_structure",
            new_name="descripcion",
        ),
        migrations.RemoveField(
            model_name="template",
            name="resume",
        ),
        migrations.RemoveField(
            model_name="template",
            name="styles",
        ),
        migrations.AddField(
            model_name="resume",
            name="template_selected",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="resumes",
                to="resume_app.template",
            ),
        ),
        migrations.AddField(
            model_name="template",
            name="componet_name",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="template",
            name="customazation_rules",
            field=models.JSONField(default=list),
        ),
        migrations.CreateModel(
            name="ResumeTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("custom_styles", models.JSONField(default=list)),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume_app.resume",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume_app.template",
                    ),
                ),
            ],
        ),
    ]
