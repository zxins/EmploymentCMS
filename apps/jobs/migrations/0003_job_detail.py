# Generated by Django 3.1.2 on 2020-10-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_job_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='detail',
            field=models.TextField(default='', verbose_name='职位详情'),
        ),
    ]
