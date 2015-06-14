# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('storage_limit', models.IntegerField(default=100000)),
                ('base_path', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('used', models.BooleanField(default=False)),
                ('permission', models.ForeignKey(to='website.Permission')),
            ],
        ),
    ]
