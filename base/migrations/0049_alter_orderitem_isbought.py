# Generated by Django 4.1.7 on 2023-04-06 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_alter_product_isbought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='isBought',
            field=models.BooleanField(default=False),
        ),
    ]