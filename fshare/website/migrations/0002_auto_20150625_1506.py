# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationkey',
            name='distributed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fsuser',
            name='user',
            field=models.OneToOneField(related_name='fshare_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='permission',
            name='base_path',
            field=models.CharField(max_length=1024, default='/tmp'),
        ),
    ]
