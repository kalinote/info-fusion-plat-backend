# Generated by Django 4.2.4 on 2023-11-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider_management', '0005_rssparamstemplate_deploy_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssparamstemplate',
            name='schedules_id',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
