from django.db import models


class Subscription(models.Model):
    level = models.IntegerField(verbose_name='уровень')
    price = models.FloatField(verbose_name='стоимость')

    min_shift = models.IntegerField(verbose_name='минимальная задержка в секундах')
    max_shift = models.IntegerField(verbose_name='максимальная задержка в секундах')
    maximum_request_duration = models.IntegerField(verbose_name='максимальная длительность запроса')

    def settings(self):
        """
        настройки для пользователя
        """
        return {
            'max_minutes': self.maximum_request_duration,
            'min_shift' : self.min_shift, 
            'max_shift' : self.max_shift
        }

    @property
    def description(self):
        """
        описание подписки
        """
        return f"""
        Минимальная-максимальная задержка: {self.min_shift} - {self.max_shift} секунд.\n
        Максимальная длительность запроса: {self.maximum_request_duration} минут.
        """
                
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f"Level {self.level} | Price {self.price}$"
