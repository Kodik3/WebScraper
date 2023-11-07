# Python.
from datetime import datetime as dt
import time
# Django.
from django.conf import settings
# models.
from .models import (
    CastomUser, 
    DataPageRequest
)
# Celery.
from settings.celery import app
from celery import shared_task
# Local.
from main.utils import GetHtml
from abstracts.utils import send_email

#! ДОБАВИТЬ ССЫЛКИ !!!!!!!!!!!

@app.task
def subscription_verification():
    #! функция для проверки подписки у всех пользователей
    #! будет отробатывать каждый день и убирать подписки 
    #! пользователей у которых подписка закончилась
    today = dt.now().date()
    to_emails: list = []
    users = CastomUser.objects.filter(subscription=True, subscription_end_date=today)
    for user in users:
        user.subscription = False
        to_emails.append(user.email)
        user.save(update_fields=['subscription'])
    
    #? будет отсылатся сообщение на эл. почту.
    if to_emails:
        return send_email(
            header=f'| {settings.SITE_NAME} | У вас закончилась подписка',
            msg='Вы можете обновить подписку на странице {}'.format('тут будет ссылка на страницу покупки подписки'),
            to_emails=to_emails
        )
    else: return None
    
@app.task
def finish_sub(user, *args, **kwargs):
    #! пользователь купил подписку и через 30 дней функция сробатывает
    if user.subscription:
        user.subscription = False
        user.subscription_level = 0
        user.save(update_fields=['subscription', 'subscription_level'])
        send_email(
            header=f"| {settings.SITE_NAME} | У вас закончилась подписка",
            msg='Вы можете обновить подписку на странице <a href="{}"></a>'.format('тут будет ссылка на страницу покупки подписки'),
            to_emails=[user.email]
        )
