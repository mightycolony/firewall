# Generated by Django 4.1 on 2023-11-05 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_adding', '0007_alter_lastpk_postrouting_last_pk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastpk',
            name='postrouting_last_pk',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='lastpk',
            name='prerouting_last_pk',
            field=models.IntegerField(default=1),
        ),
    ]
