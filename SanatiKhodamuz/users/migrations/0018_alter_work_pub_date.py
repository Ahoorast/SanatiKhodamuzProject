# Generated by Django 4.1.1 on 2022-09-20 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_work_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 17, 44, 19, 608327, tzinfo=datetime.timezone.utc), verbose_name='date published'),
        ),
    ]
