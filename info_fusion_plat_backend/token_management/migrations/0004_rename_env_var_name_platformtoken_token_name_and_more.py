# Generated by Django 4.2.4 on 2023-10-27 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('token_management', '0003_platformtoken_is_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformtoken',
            old_name='env_var_name',
            new_name='token_name',
        ),
        migrations.RenameField(
            model_name='platformtoken',
            old_name='value',
            new_name='token_value',
        ),
    ]
