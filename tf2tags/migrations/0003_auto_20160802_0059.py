# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf2tags', '0002_auto_20150809_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='admin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='users',
            name='bonus_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='users',
            name='bonus_submitted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='users',
            name='last_visit',
            field=models.DateField(default='2011-04-01', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='max_posted_comments',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='users',
            name='posted_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to='tf2tags.Users', null=True, on_delete=models.SET_NULL),
        ),
    ]
