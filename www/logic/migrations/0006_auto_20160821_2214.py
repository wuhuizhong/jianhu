# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0005_auto_20160821_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='district',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AddField(
            model_name='job',
            name='province',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AlterField(
            model_name='job',
            name='city',
            field=models.CharField(default='', max_length=18),
        ),
    ]
