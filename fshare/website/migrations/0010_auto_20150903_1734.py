# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20150902_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='max_dl',
            field=models.IntegerField(default=1, blank=True, null=True),
        ),
    ]
