# Generated by Django 3.1.2 on 2020-10-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0002_enterprises_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprises',
            name='address',
            field=models.CharField(default='', max_length=200, verbose_name='地址'),
        ),
    ]
