# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20160814_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='real_key',
            field=models.CharField(default=None, max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='storage_limit',
            field=models.IntegerField(default=209715200),
        ),
    ]
