# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-14 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_bind_mycollection_myinterview_myrecommend_profile_profileext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bind',
            name='wx_openid',
            field=models.CharField(db_index=True, max_length=36),
        ),
        migrations.AlterField(
            model_name='profile',
            name='portrait',
            field=models.CharField(max_length=256),
        ),
    ]
