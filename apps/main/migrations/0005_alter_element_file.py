# Generated by Django 4.2.6 on 2023-11-23 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_element_delete_jsonelement_delete_textelement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='file',
            field=models.FileField(null=True, upload_to='result_data/elements/', verbose_name='данные'),
        ),
    ]
