# Generated by Django 2.2.4 on 2019-08-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleengine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleengine',
            name='rule_type',
            field=models.SmallIntegerField(choices=[(1, 'equal'), (2, 'upper'), (3, 'lower'), (4, 'in range'), (5, 'out range'), (6, 'null')], default=1),
        ),
    ]
