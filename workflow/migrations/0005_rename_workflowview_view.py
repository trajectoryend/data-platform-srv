# Generated by Django 5.0.4 on 2024-05-08 05:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
        ('workflow', '0004_remove_workflowtype_created_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorkFlowView',
            new_name='View',
        ),
    ]
