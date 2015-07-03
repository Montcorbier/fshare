# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150625_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationkey',
            name='revoked',
            field=models.BooleanField(default=False),
        ),
    ]
