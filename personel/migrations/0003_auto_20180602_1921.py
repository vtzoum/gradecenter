# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-02 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0002_auto_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='phoneHom',
            field=models.CharField(default=b'26410', max_length=14),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='statusTime',
            field=models.DateTimeField(blank=True, default=b'2018-06-02 19:21:22'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='actionTime',
            field=models.DateTimeField(default=b'2018-06-02 19:21:22'),
        ),
    ]
