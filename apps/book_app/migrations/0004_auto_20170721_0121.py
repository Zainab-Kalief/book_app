# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-21 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0003_auto_20170720_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='average_rating',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(max_length=100),
        ),
    ]
