# Generated by Django 4.1.7 on 2023-04-15 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_sport_gaming'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='gaming',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.gaming'),
        ),
        migrations.AddField(
            model_name='review',
            name='sport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.sport'),
        ),
    ]
