# Generated by Django 5.1.4 on 2025-02-18 21:00

import resume_app.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0019_alter_experience_summary_alter_experience_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='highlights',
            field=models.JSONField(default=list, help_text='Lista de Aspectos destacados del trabajo.', null=True, validators=[resume_app.utils.check_list_does_not_exceed_50]),
        ),
        migrations.AlterField(
            model_name='skill',
            name='keywords',
            field=models.JSONField(default=list, help_text='Palabras clave asociadas a la habilidad.', null=True, validators=[resume_app.utils.check_list_does_not_exceed_50]),
        ),
    ]
