# Generated by Django 4.1.3 on 2022-11-23 12:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_alter_files_up_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="files",
            name="up_time",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 11, 23, 14, 32, 16, 15197)
            ),
        ),
        migrations.CreateModel(
            name="Phones",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.addressbook",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Emails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mail", models.CharField(max_length=254, unique=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.addressbook",
                    ),
                ),
            ],
        ),
    ]
