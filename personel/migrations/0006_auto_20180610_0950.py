# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-10 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0005_auto_20180608_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='statusTime',
            field=models.DateTimeField(blank=True, default=b'2018-06-10 09:50:47'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='actionTime',
            field=models.DateTimeField(default=b'2018-06-10 09:50:47'),
        ),
    ]