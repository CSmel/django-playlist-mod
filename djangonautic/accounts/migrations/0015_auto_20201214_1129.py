# Generated by Django 2.2.17 on 2020-12-14 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20201213_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='profile.png', upload_to='media/'),
        ),
    ]
