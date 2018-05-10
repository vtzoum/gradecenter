# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-08 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0081_auto_20170608_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='SchoolToGradeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personel.SchoolToGrade'),
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='statusTime',
            field=models.DateTimeField(blank=True, default=b'2017-06-08 22:05:00'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='actionTime',
            field=models.DateTimeField(default=b'2017-06-08 22:05:00'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='acceptances',
            field=models.ManyToManyField(through='personel.Acceptance', to='personel.SchoolToGrade'),
        ),
    ]
