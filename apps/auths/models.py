from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from subscription.models import Subscription


class CastomUserManager(BaseUserManager):
    def create_user(self, email: str, password:str=None, **kwargs):
        if not email:
            raise ValidationError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password:str=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)
    

class CastomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя

    Параметры:
        - email (EmailField)
        - name (str)
        - password (str)
        - is_staff (bool)

    Параметры подписки:
        - free_subscription_is_use (bool): Использовал ли бесплатную подписку.
        - subscription (bool): Действительна ли подписка.
        - subscription_level (int): Уровень подписки.
        - subscription_end_date (DateField): Дата окончания подписки.
    """
    class SubLevel(models.IntegerChoices):
        level_0 = 0
        level_1 = 1
        level_2 = 2
        level_3 = 3
    
    email = models.EmailField(verbose_name='почта/логин', max_length=200, unique=True)
    name = models.CharField(verbose_name='имя', max_length=100)
    password = models.CharField(verbose_name='пароль', max_length=60, unique=True)
    is_staff: bool = models.BooleanField(default=False)

    free_subscription_is_use = models.BooleanField(default=False, verbose_name='бесплатная подписка')
    subscription = models.BooleanField(default=False, verbose_name='подписка')
    subscription_level = models.IntegerField(choices=SubLevel.choices, blank=True, null=True, default=0)
    subscription_end_date = models.DateField(verbose_name='дата окончания', blank=True, null=True)
    
    objects = CastomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.email


class PageRequests(models.Model):
    """
    Модель настроек запроса

    Параметры:
        - user (CastomUser): Модель пользователя.
        - url (str): URL куда будет поступать запрос.
        - duration_minutes (int): Длительность запроса в минутах.
        - shift (int): Задержка после каждого запроса в секундах.
        - content_type (str): Тип контента.
        - send_email (bool): Отправка сообщение пользователю после завершения запроса.
        - id_name (str): Название id котрые будем собирать.
        - class_name (str): Название class котрые будем собирать.
    """
    class FileType(models.Choices):
        txt = 'txt'
        json = 'json'
        
    user = models.ForeignKey(to=CastomUser, verbose_name='пользователь', on_delete=models.CASCADE)
    url = models.CharField(verbose_name='ссылка', max_length=200)
    duration_minutes = models.IntegerField(verbose_name='длительность в минутах')
    shift = models.IntegerField(verbose_name='сдвиг')
    content_type = models.CharField(verbose_name='тип контента', choices=FileType.choices, max_length=10)
    send_email = models.BooleanField(default=False)
    
    id_name = models.CharField(verbose_name='id', blank=True, null=True, default=None, max_length=200)
    class_name = models.CharField(verbose_name='class', blank=True, null=True, default=None, max_length=200)


class DataPageRequest(models.Model):
    """
    Модель для хранения данных с запросов

    Параметры:
        - user (CastomUser): Модель пользователя.
        - data (str): Данные.
        - content_type (str): Тип контента.
    """
    user = models.ForeignKey(to=CastomUser, verbose_name='пользователь', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название', max_length=200, null=True, blank=True)
    data = models.CharField(verbose_name="данные", max_length=1000)
    file = models.FileField(verbose_name='данные', upload_to='result_data/page_requests/', null=True, blank=True)
    content_type = models.CharField(verbose_name='тип контента', max_length=10, default='')
    date_create = models.DateField(verbose_name='дата создания', auto_now_add=True, blank=True, null=True)
