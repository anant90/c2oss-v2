# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='github_access_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]