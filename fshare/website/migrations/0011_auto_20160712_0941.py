# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20150903_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_list',
            field=models.CharField(null=True, max_length=1024, blank=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='max_dl',
            field=models.IntegerField(default=1),
        ),
    ]
