# Generated by Django 4.1.3 on 2022-11-23 18:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0007_emails_user_id_phones_user_id_alter_files_up_time"),
    ]

    operations = [
        migrations.RenameField(
            model_name="emails",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="phones",
            old_name="user_id",
            new_name="user",
        ),
        migrations.AlterField(
            model_name="files",
            name="up_time",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 11, 23, 20, 24, 47, 378967)
            ),
        ),
    ]
