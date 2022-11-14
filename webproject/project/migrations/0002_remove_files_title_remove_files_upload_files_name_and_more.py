# Generated by Django 4.1.3 on 2022-11-14 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='title',
        ),
        migrations.RemoveField(
            model_name='files',
            name='upload',
        ),
        migrations.AddField(
            model_name='files',
            name='name',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='files',
            name='type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='up_id',
            field=models.CharField(max_length=35, null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='up_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 23, 7, 31, 593659)),
        ),
    ]
