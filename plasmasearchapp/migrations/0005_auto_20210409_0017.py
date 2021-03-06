# Generated by Django 3.0.8 on 2021-04-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plasmasearchapp', '0004_auto_20210409_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=30),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='quartype',
            field=models.CharField(choices=[('hospitalized', 'hospitalized'), ('homequar', 'Home Quarantined')], max_length=30),
        ),
    ]
