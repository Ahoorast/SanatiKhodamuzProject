# Generated by Django 4.1.1 on 2022-09-20 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_work_estimate'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 17, 42, 8, 815718, tzinfo=datetime.timezone.utc), verbose_name='date published'),
        ),
    ]
