# Generated by Django 4.2.7 on 2023-11-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_adding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastpk',
            name='postrouting_last_pk',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lastpk',
            name='prerouting_last_pk',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
