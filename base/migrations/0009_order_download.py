# Generated by Django 4.1.7 on 2023-03-28 15:08

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_review_createdat'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='download',
            field=models.FileField(blank=True, null=True, upload_to=base.models.upload_image_path),
        ),
    ]