# Generated by Django 5.0.1 on 2024-01-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPPMS', '0002_alter_passwordreset_validtill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalmodel',
            name='comment',
            field=models.CharField(max_length=133234250),
        ),
        migrations.AlterField(
            model_name='proposalmodel',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='proposalmodel',
            name='pdesc',
            field=models.CharField(max_length=2323250),
        ),
        migrations.AlterField(
            model_name='proposalmodel',
            name='phone',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='proposalmodel',
            name='userType',
            field=models.CharField(default='other', max_length=250),
        ),
    ]
