# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20150831_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='expiration_date',
            field=models.DateTimeField(null=True, blank=True, default=None),
        ),
    ]
