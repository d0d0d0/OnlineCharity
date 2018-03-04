# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20160210_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='tc_no',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
