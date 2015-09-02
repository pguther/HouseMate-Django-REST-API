# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150901_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chore',
            name='claimed_by',
            field=models.CharField(default='', blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='chore',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chore',
            name='due_day',
            field=models.TextField(default='Sunday', max_length=10),
        ),
        migrations.AddField(
            model_name='chore',
            name='expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chore',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
