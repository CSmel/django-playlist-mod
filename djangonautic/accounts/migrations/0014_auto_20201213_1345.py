# Generated by Django 2.2.17 on 2020-12-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20201213_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='profile.png', upload_to='media/'),
        ),
    ]
