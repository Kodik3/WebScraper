# Generated by Django 4.2.6 on 2023-12-07 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0007_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]