# Generated by Django 4.1.1 on 2022-09-18 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_work_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]