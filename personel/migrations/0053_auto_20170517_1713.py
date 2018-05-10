# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-17 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0052_auto_20170517_1632'),
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
            field=models.DateTimeField(blank=True, default=b'2017-05-17 17:13:48'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='actionTime',
            field=models.DateTimeField(default=b'2017-05-17 17:13:48'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='acceptances',
            field=models.ManyToManyField(through='personel.Acceptance', to='personel.SchoolToGrade'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='type',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='schooltograde',
            name='type',
            field=models.SmallIntegerField(choices=[(0, b'\xce\x97\xce\x9c\xce\x95\xce\xa1\xce\x97\xce\xa3\xce\x99\xce\x9f'), (1, b'\xce\x95\xce\xa3\xce\xa0\xce\x95\xce\xa1\xce\x99\xce\x9d\xce\x9f')], default=0),
        ),
    ]
