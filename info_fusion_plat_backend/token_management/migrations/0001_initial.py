# Generated by Django 4.2.4 on 2023-08-19 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('env_var_name', models.CharField(max_length=100, unique=True)),
                ('value', models.CharField(max_length=5000)),
                ('platform', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, null=True)),
                ('is_using', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '平台token',
                'verbose_name_plural': '平台token',
                'db_table': 'platform_token',
                'ordering': ['id'],
            },
        ),
    ]
