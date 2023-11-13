from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


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
    class SubLevel(models.Choices):
        level_0 = 0
        level_1 = 1
        level_2 = 2
        level_3 = 3
        
    email = models.EmailField(verbose_name='почта/логин', max_length=200, unique=True)
    name = models.CharField(verbose_name='имя', max_length=100)
    password = models.CharField(verbose_name='пароль', max_length=60, unique=True)
    is_staff: bool = models.BooleanField(default=False)

    #* подписка
    subscription: bool = models.BooleanField(default=False, verbose_name='подписка')
    subscription_end_date = models.DateField(verbose_name='дата окончания', blank=True, null=True)
    subscription_level = models.IntegerField(choices=SubLevel.choices, blank=True, null=True, default=0)
    
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
    class FileType(models.Choices):
        txt = 'txt'
        json = 'json'
        
    user = models.ForeignKey(to=CastomUser, verbose_name='пользователь', on_delete=models.CASCADE)
    url = models.CharField(verbose_name='ссылка', max_length=200)
    duration_minutes = models.IntegerField(verbose_name='длительность в минутах')
    shift = models.IntegerField(verbose_name='сдвиг') #* то есть через сколько минут будет отробатывть
    content_type = models.CharField(verbose_name='тип контента', choices=FileType.choices, max_length=10)
    send_email = models.BooleanField(default=False)
    
    id_name = models.CharField(verbose_name='id', blank=True, null=True, default=None, max_length=200)
    class_name = models.CharField(verbose_name='class', blank=True, null=True, default=None, max_length=200)


class DataPageRequest(models.Model):
    user = models.ForeignKey(to=CastomUser, verbose_name='пользователь', on_delete=models.CASCADE)
    data = models.CharField(verbose_name="данные", max_length=1000)
    content_type = models.CharField(verbose_name='тип контента', max_length=10)
    date_create = models.DateField(verbose_name='дата создания',auto_now_add=True)
