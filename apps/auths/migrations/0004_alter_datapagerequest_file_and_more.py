# Generated by Django 4.2.6 on 2023-11-24 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_datapagerequest_file_datapagerequest_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapagerequest',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='result_data/page_requests/', verbose_name='данные'),
        ),
        migrations.AlterField(
            model_name='datapagerequest',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='название'),
        ),
    ]
