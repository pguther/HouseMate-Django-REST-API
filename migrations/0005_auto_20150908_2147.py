# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150901_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='claimed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='assigned_chores'),
        ),
        migrations.AlterField(
            model_name='chore',
            name='due_day',
            field=models.TextField(max_length=10, default=''),
        ),
    ]
