# Generated by Django 5.1.4 on 2025-03-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0024_rename_customazation_rules_template_customization_rules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumecustomization',
            name='custom_styles',
            field=models.JSONField(default=dict, help_text='Estilos personalizados aplicados al resumen.'),
        ),
        migrations.AlterField(
            model_name='template',
            name='customization_rules',
            field=models.JSONField(default=dict, help_text='Reglas de personalización de la plantilla.'),
        ),
    ]
