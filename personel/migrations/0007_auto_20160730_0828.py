# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-30 08:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0006_auto_20160730_0739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='lessonF',
            new_name='LessonID',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='no',
            new_name='bookCount',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='place',
            new_name='folderStatus',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='status',
            new_name='isNow',
        ),
        migrations.RenameField(
            model_name='registry',
            old_name='folderF',
            new_name='FolderID',
        ),
        migrations.RenameField(
            model_name='registry',
            old_name='graderF',
            new_name='GraderID',
        ),
        migrations.RenameField(
            model_name='registry',
            old_name='status',
            new_name='isNow',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='registers',
        ),
        migrations.RemoveField(
            model_name='registry',
            name='no',
        ),
        migrations.AddField(
            model_name='folder',
            name='folderNo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registry',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 30, 8, 28, 15, 145784, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registry',
            name='regAction',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='registry',
            name='regStatus',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
