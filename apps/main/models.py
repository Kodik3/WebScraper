from django.db import models


class JsonElement(models.Model):
    name = models.CharField(verbose_name='название', max_length=130)
    file = models.FileField(verbose_name='данные', upload_to='result_data/json/', null=True)


class TextElement(models.Model):
    name = models.CharField(verbose_name='название', max_length=130)
    file = models.FileField(verbose_name='данные', upload_to='result_data/text/', null=True)
