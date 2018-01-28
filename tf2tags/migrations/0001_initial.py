# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('steamID', models.CharField(max_length=20)),
                ('notes', models.CharField(max_length=150)),
                ('begins', models.DateTimeField(auto_now_add=True, verbose_name=b'Ban Start')),
                ('ends', models.DateTimeField(verbose_name=b'Ban End')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemID', models.IntegerField(db_index=True)),
                ('ip', models.IPAddressField()),
                ('comment', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theme', models.CharField(max_length=50)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('winner', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Flagged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemID', models.IntegerField()),
                ('type', models.CharField(max_length=20)),
                ('explanation', models.CharField(max_length=500)),
                ('handled', models.CharField(max_length=100)),
                ('ip', models.IPAddressField()),
                ('steamID', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(default=b'Dr. Dos', max_length=50)),
                ('profile', models.CharField(default=b'id/dr_dos', max_length=50)),
                ('image', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=8000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set', models.CharField(default=0, max_length=50)),
                ('defindex', models.CharField(max_length=5, db_index=True)),
                ('role', models.CharField(max_length=8, db_index=True)),
                ('slot', models.CharField(max_length=9, db_index=True)),
                ('base', models.CharField(max_length=200, db_index=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('desc', models.CharField(default=b'', max_length=200, verbose_name=b'description', db_index=True)),
                ('prefix', models.CharField(default=b'', max_length=50)),
                ('filter', models.CharField(default=b'', max_length=50)),
                ('color', models.CharField(default=b'FFD700', max_length=6)),
                ('paint', models.CharField(default=b'', max_length=6)),
                ('particles', models.CharField(default=b'', max_length=50)),
                ('style', models.IntegerField(default=0)),
                ('keywords', models.CharField(default=b'', max_length=500, db_index=True)),
                ('ip', models.IPAddressField(default=b'')),
                ('upVotes', models.IntegerField(default=0)),
                ('downVotes', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0, db_index=True)),
                ('comments', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('steamID', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=32)),
                ('profile', models.CharField(max_length=200)),
                ('avatar', models.CharField(max_length=200)),
                ('submitted', models.IntegerField(default=0)),
                ('maxSubmitted', models.IntegerField(default=5)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemID', models.IntegerField()),
                ('ip', models.IPAddressField()),
                ('vote', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='submissions',
            name='user',
            field=models.ForeignKey(to='tf2tags.Users', on_delete=models.SET_DEFAULT),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(to='tf2tags.Users', on_delete=models.CASCADE),
        ),
    ]
