# Generated by Django 4.1.1 on 2022-09-18 17:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_work_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 18, 17, 51, 41, 892393, tzinfo=datetime.timezone.utc), verbose_name='date published'),
        ),
    ]
