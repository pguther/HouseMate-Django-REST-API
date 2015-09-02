# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150901_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
