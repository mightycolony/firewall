# Generated by Django 4.2.7 on 2023-11-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_fetcher_display', '0007_alter_userprofileinfo_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=5)),
                ('ip', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
