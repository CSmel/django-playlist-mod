# Generated by Django 2.2.17 on 2021-01-09 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timecards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payrolltotal',
            name='identifier',
        ),
    ]
