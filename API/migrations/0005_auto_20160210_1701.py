# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20160210_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='mid',
            field=models.IntegerField(default=1000000000, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='mid',
            field=models.IntegerField(default=1000000000, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='tc_no',
            field=models.IntegerField(unique=True),
        ),
    ]
