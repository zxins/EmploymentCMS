# Generated by Django 3.1.2 on 2020-11-01 23:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0004_auto_20201101_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='mix_salary',
        ),
        migrations.AddField(
            model_name='jobs',
            name='min_salary',
            field=models.FloatField(default=0, help_text='单位：K', max_length=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='最小薪资'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='education',
            field=models.CharField(choices=[(0, '高中'), (1, '大专'), (2, '本科'), (3, '硕士'), (4, '博士')], default='', max_length=10, verbose_name='学历'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='max_salary',
            field=models.FloatField(default=0, help_text='单位：K', max_length=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='最小薪资'),
        ),
    ]
