# Generated by Django 4.2.6 on 2023-10-27 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JsonElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=130, verbose_name='название')),
                ('file', models.FileField(null=True, upload_to='result_data/json/', verbose_name='данные')),
            ],
        ),
        migrations.CreateModel(
            name='TextElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=130, verbose_name='название')),
                ('file', models.FileField(null=True, upload_to='result_data/text/', verbose_name='данные')),
            ],
        ),
        migrations.DeleteModel(
            name='Element',
        ),
    ]
