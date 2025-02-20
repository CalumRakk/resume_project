# Generated by Django 5.1.4 on 2025-02-20 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0022_resumecustomization_unique_resume_template_customization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experience',
            options={'verbose_name': 'Experiencia', 'verbose_name_plural': 'Experiencias'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'Habilidad', 'verbose_name_plural': 'Habilidades'},
        ),
        migrations.RemoveConstraint(
            model_name='experience',
            name='unique_order_per_resume_experience',
        ),
        migrations.RemoveConstraint(
            model_name='skill',
            name='unique_order_per_resume_skill',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='order',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='order',
        ),
    ]
