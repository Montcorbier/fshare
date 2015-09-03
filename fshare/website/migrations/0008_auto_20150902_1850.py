# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20150831_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='iv',
            field=models.CharField(null=True, max_length=16, blank=True),
        ),
        migrations.AddField(
            model_name='file',
            name='key',
            field=models.CharField(null=True, max_length=64, blank=True, verbose_name='Key'),
        ),
    ]
