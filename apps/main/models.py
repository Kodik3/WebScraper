from django.db import models


class Element(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)
    file = models.FileField(verbose_name='данные', upload_to='result_data/elements/', null=True)
    date_create = models.DateField(auto_now_add=True, blank=True, null=True)
