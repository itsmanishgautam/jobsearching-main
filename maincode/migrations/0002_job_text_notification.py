# Generated by Django 5.0.2 on 2024-03-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='text_notification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
