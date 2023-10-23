import os
from django.core.management import call_command
os.environ.setdefault('DJANGO_SETTINGS_MODULE','firewall_project.settings')

import django
django.setup()

from rules_fetcher_display import models
models.postrouting.objects.all().delete()
models.prerouting.objects.all().delete()



from django.db import connection

# Replace 'your_app_name' with the name of your Django app and 'postrouting' with the model name
with open('reset_sequence.sql', 'w') as f:
    cursor = connection.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'rules_fetcher_display_postrouting'")
    table_create_sql = cursor.fetchone()[0]
    f.write(table_create_sql)


with open('reset_sequence.sql', 'r') as f:
    create_table_sql = f.read()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS rules_fetcher_display_postrouting")
    cursor.execute(create_table_sql)


with open('reset_sequence.sql', 'w') as f:
    cursor = connection.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'rules_fetcher_display_prerouting'")
    table_create_sql = cursor.fetchone()[0]
    f.write(table_create_sql)


with open('reset_sequence.sql', 'r') as f:
    create_table_sql = f.read()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS rules_fetcher_display_prerouting")
    cursor.execute(create_table_sql)