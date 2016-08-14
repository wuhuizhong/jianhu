# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-14 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_id', models.IntegerField(db_index=True)),
                ('user_id', models.IntegerField()),
                ('words', models.CharField(max_length=120)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'conversation',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, max_length=36)),
                ('user_id', models.IntegerField(db_index=True)),
                ('company_name', models.CharField(max_length=20)),
                ('job_title', models.CharField(max_length=20)),
                ('work_experience', models.CharField(max_length=10)),
                ('salary', models.CharField(max_length=10)),
                ('education', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=10)),
                ('skill', models.CharField(max_length=120)),
                ('piclist', models.CharField(max_length=120)),
                ('is_valid', models.BooleanField(default=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='MergeMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(db_index=True)),
                ('from_user_id', models.IntegerField()),
                ('conversation_id', models.IntegerField()),
                ('payload', models.CharField(max_length=60)),
                ('words', models.CharField(max_length=120)),
                ('msg_type', models.CharField(choices=[('N', '\u6b63\u5e38\u6d88\u606f'), ('RR', '\u63a8\u8350\u5f55\u97f3\u6d88\u606f'), ('JS', '\u76f8\u5173\u5de5\u4f5c\u72b6\u6001\u53d8\u66f4\u6d88\u606f')], max_length=2)),
                ('update_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'merge_msg',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_uuid', models.CharField(db_index=True, max_length=36)),
                ('from_user_id', models.IntegerField(db_index=True)),
                ('to_user_id', models.IntegerField(db_index=True)),
                ('last_share_id', models.IntegerField()),
                ('sound_record_to_hr', models.CharField(max_length=40)),
                ('sound_record_to_object', models.CharField(max_length=40)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logic.Job')),
            ],
            options={
                'db_table': 'job_share',
            },
        ),
        migrations.CreateModel(
            name='VipJobList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.IntegerField(db_index=True)),
                ('user_id', models.IntegerField(unique=True)),
                ('pub_time', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'job_for_vip_list',
            },
        ),
    ]
