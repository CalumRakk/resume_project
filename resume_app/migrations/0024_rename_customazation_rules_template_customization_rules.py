# Generated by Django 5.1.4 on 2025-03-13 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0023_alter_experience_options_alter_skill_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='template',
            old_name='customazation_rules',
            new_name='customization_rules',
        ),
    ]
