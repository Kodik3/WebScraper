# Generated by Django 4.2.6 on 2023-12-07 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0006_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(verbose_name='уровень')),
                ('price', models.FloatField(verbose_name='стоимость')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
    ]
