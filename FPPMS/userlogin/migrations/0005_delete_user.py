# Generated by Django 5.0.1 on 2024-03-26 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0004_rename_employee_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
