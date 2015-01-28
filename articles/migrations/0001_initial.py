# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=1000, verbose_name='title')),
                ('preface', models.CharField(max_length=10000, verbose_name='preface')),
                ('content', models.TextField(max_length=500000, verbose_name='content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
