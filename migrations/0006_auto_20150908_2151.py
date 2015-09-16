# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150908_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='claimed_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='assigned_chores', blank=True),
        ),
    ]
