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
                ('id', models.CharField(max_length=14, primary_key=True, unique=True, serialize=False, db_index=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('private_label', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True, default='')),
                ('path', models.CharField(max_length=1024)),
                ('checksum', models.CharField(max_length=128)),
                ('size', models.IntegerField()),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('nb_hits', models.IntegerField(default=0)),
                ('nb_dl', models.IntegerField(default=0)),
                ('is_private', models.BooleanField(default=False)),
                ('pwd_hash', models.CharField(max_length=512, null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FSUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('storage_limit', models.IntegerField(default=100000)),
                ('base_path', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('key', models.CharField(max_length=100)),
                ('used', models.BooleanField(default=False)),
                ('permission', models.ForeignKey(to='website.Permission')),
            ],
        ),
        migrations.AddField(
            model_name='fsuser',
            name='permission',
            field=models.ForeignKey(to='website.Permission'),
        ),
        migrations.AddField(
            model_name='fsuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
