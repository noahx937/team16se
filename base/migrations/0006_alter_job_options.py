# Generated by Django 5.1.1 on 2024-12-07 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_name_job_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-updated', '-created']},
        ),
    ]