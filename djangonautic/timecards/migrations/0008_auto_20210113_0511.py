# Generated by Django 2.2.17 on 2021-01-13 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecards', '0007_auto_20210113_0507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payrolltotal',
            name='identifier',
        ),
        migrations.AddField(
            model_name='payrolltotal',
            name='id',
            field=models.AutoField(auto_created=True, default=1987, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
