# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20150827_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='expiration_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='file',
            name='max_dl',
            field=models.IntegerField(default=1),
        ),
    ]
