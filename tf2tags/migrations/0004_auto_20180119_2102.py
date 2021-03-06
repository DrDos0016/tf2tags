# Generated by Django 2.0.1 on 2018-01-19 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tf2tags', '0003_auto_20160802_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='users',
            name='bonus_comments',
        ),
        migrations.RemoveField(
            model_name='users',
            name='bonus_submitted',
        ),
        migrations.RemoveField(
            model_name='users',
            name='last_visit',
        ),
        migrations.AlterField(
            model_name='bans',
            name='begins',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ban Start'),
        ),
        migrations.AlterField(
            model_name='bans',
            name='ends',
            field=models.DateTimeField(verbose_name='Ban End'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.CharField(default='Dr. Dos', max_length=50),
        ),
        migrations.AlterField(
            model_name='news',
            name='profile',
            field=models.CharField(default='id/dr_dos', max_length=50),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='color',
            field=models.CharField(default='FFD700', max_length=6),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='desc',
            field=models.CharField(db_index=True, default='', max_length=200, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='filter',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='ip',
            field=models.GenericIPAddressField(default=''),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='keywords',
            field=models.CharField(db_index=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='paint',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='particles',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='prefix',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='tf2tags.Users'),
        ),
        migrations.AlterField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tf2tags.Users'),
        ),
    ]
