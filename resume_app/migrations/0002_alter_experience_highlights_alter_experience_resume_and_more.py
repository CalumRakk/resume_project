# Generated by Django 5.1.4 on 2024-12-11 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='highlights',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='experience',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='resume_app.resume'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='keywords',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='skill',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='resume_app.resume'),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('html_structure', models.TextField()),
                ('styles', models.JSONField(default=dict)),
                ('resume', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='template', to='resume_app.resume')),
            ],
        ),
    ]
