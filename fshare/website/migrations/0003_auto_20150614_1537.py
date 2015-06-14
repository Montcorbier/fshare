# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('website', '0002_permission_registrationkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSUser',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, auto_created=True, serialize=False, parent_link=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='permission',
            name='id',
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(primary_key=True, serialize=False, max_length=255),
        ),
        migrations.AddField(
            model_name='fsuser',
            name='permission',
            field=models.ForeignKey(to='website.Permission'),
        ),
    ]
