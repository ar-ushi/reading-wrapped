# Generated by Django 5.0.1 on 2024-01-28 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrapped', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdata',
            name='readingstats',
            field=models.JSONField(default=dict),
        ),
    ]
