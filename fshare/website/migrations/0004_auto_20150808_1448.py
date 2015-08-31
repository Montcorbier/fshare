# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_registrationkey_revoked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='pwd_hash',
        ),
        migrations.AddField(
            model_name='file',
            name='pwd',
            field=models.CharField(verbose_name='Key', max_length=512, null=True, blank=True),
        ),
    ]
