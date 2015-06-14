# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.CharField(primary_key=True, db_index=True, serialize=False, max_length=14, unique=True)),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('private_label', models.CharField(blank=True, null=True, max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('path', models.CharField(max_length=1024)),
                ('checksum', models.CharField(max_length=128)),
                ('size', models.IntegerField()),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('nb_hits', models.IntegerField(default=0)),
                ('nb_dl', models.IntegerField(default=0)),
                ('is_private', models.BooleanField(default=False)),
                ('pwd_hash', models.CharField(blank=True, null=True, max_length=512)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
