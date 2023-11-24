# Generated by Django 4.2.6 on 2023-11-23 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_castomuser_free_subscription_is_use_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapagerequest',
            name='file',
            field=models.FileField(null=True, upload_to='result_data/page_requests/', verbose_name='данные'),
        ),
        migrations.AddField(
            model_name='datapagerequest',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='datapagerequest',
            name='date_create',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='дата создания'),
        ),
    ]
