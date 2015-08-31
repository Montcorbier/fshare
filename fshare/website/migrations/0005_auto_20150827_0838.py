# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20150808_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
