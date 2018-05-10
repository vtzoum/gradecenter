# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-30 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0005_auto_20160729_0824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grader',
            old_name='fidLesson',
            new_name='LessonID',
        ),
        migrations.RenameField(
            model_name='grader',
            old_name='fidTeacher',
            new_name='TeacherID',
        ),
        migrations.RenameField(
            model_name='grader',
            old_name='coordinator',
            new_name='isCoordinator',
        ),
        migrations.RenameField(
            model_name='grader',
            old_name='graderC',
            new_name='isgraderC',
        ),
        migrations.AlterField(
            model_name='school',
            name='stype',
            field=models.IntegerField(choices=[(1, b'\xce\x93\xce\xa5\xce\x9c\xce\x9d\xce\x91\xce\xa3\xce\x99\xce\x9f'), (2, b'\xce\x9b\xce\xa5\xce\x9a\xce\x95\xce\x99\xce\x9f'), (3, b'\xce\x99\xce\x94\xce\x99\xce\xa9\xce\xa4\xce\x99\xce\x9a\xce\x9f')]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='codeSpec',
            field=models.CharField(max_length=8),
        ),
    ]
