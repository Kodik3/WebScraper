# Generated by Django 4.2.6 on 2023-12-07 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0005_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]