# Generated by Django 4.2.4 on 2023-11-09 15:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spider_management', '0002_rssparamstemplate_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssparamstemplate',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rssparamstemplate',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
