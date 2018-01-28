# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf2tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bans',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='comments',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='flagged',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='ip',
            field=models.GenericIPAddressField(default=b''),
        ),
        migrations.AlterField(
            model_name='votes',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
