# Generated by Django 4.1.7 on 2023-04-01 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_plan_brand_plan_category_plan_countinstock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='createdAt',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]