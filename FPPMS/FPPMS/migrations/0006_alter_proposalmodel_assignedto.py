# Generated by Django 5.0.1 on 2024-03-29 06:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPPMS', '0005_alter_proposalmodel_assignedto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalmodel',
            name='assignedTo',
            field=models.ManyToManyField(blank=True, default='yash', related_name='assigned_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
