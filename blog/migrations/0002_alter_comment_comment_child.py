# Generated by Django 4.0 on 2022-01-01 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_child',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
    ]
