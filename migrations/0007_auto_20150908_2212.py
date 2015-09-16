# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150908_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='due_day',
            field=models.TextField(max_length=10),
        ),
    ]
