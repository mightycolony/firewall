# Generated by Django 4.1 on 2023-11-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_fetcher_display', '0008_serverdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverdetails',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]