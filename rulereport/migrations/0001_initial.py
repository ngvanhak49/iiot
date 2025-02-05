# Generated by Django 2.2.4 on 2019-08-29 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ruleengine', '0001_initial'),
        ('things', '0004_auto_20190829_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuleEngineReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=50)),
                ('value', models.CharField(blank=True, max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('ruleengine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ruleengine.RuleEngine')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='things.Thing')),
            ],
            options={
                'verbose_name': 'Rule Engine Report',
            },
        ),
    ]
