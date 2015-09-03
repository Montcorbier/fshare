# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20150902_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='key',
            field=models.CharField(verbose_name='Key', null=True, max_length=512, blank=True),
        ),
    ]
