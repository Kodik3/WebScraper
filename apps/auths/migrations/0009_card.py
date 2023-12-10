# Generated by Django 4.2.6 on 2023-12-10 03:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0008_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Number не верный формат', regex='^\\d{16}$')], verbose_name='номер')),
                ('cvv', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(message='CVV не верный формат', regex='^\\d{3}$')], verbose_name='номер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Карта',
                'verbose_name_plural': 'Карты',
                'ordering': ('-id',),
            },
        ),
    ]