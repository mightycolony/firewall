# Generated by Django 4.2.7 on 2023-11-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_adding', '0008_alter_lastpk_postrouting_last_pk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastpk',
            name='postrouting_last_pk',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lastpk',
            name='prerouting_last_pk',
            field=models.IntegerField(default=0),
        ),
    ]