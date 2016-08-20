# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20160712_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='max_dl_limit',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='permission',
            name='max_expiration_delay',
            field=models.IntegerField(default=30),
        ),
    ]
