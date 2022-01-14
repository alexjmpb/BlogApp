# Generated by Django 4.0 on 2022-01-09 22:30

import authentication.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userblog',
            name='user_image',
            field=models.ImageField(default='users/default_user.jpg', upload_to=authentication.models.user_images_path, validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
