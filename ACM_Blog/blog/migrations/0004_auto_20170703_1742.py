# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-03 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170703_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='profile_image',
            field=models.ImageField(default='blog/static/blog/images/images.jpg', upload_to='blog/static/images/'),
        ),
    ]