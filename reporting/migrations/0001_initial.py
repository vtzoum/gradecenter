# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-09 14:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['county', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('max_temperature', models.FloatField()),
                ('min_temperature', models.FloatField()),
                ('wind_speed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='wind speed')),
                ('precipitation', models.IntegerField(verbose_name='precipitation')),
                ('precipitation_probability', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='precipitation probability')),
                ('observations', models.TextField(verbose_name='weather observations')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='town', to='reporting.Town')),
            ],
            options={
                'ordering': ['-date', 'town'],
                'verbose_name_plural': 'weather',
            },
        ),
        migrations.AlterUniqueTogether(
            name='weather',
            unique_together=set([('town', 'date')]),
        ),
    ]
