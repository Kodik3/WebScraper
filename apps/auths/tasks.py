# Python.
from datetime import timedelta
# Django.
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# models.
from .models import DataPageRequest, CastomUser
# Celery.
from settings.celery import app
# Local.
from abstracts.utils import send_email


def subscription_link():
    return f"""<a href="{reverse('buy_sub')}">подписки</a>"""

# @app.task
# def subscription_verification():
#     #! функция для проверки подписки у всех пользователей
#     #! будет отробатывать каждый день и убирать подписки 
#     #! пользователей у которых подписка закончилась
#     today = dt.now().date()
#     to_emails: list = []
#     users = CastomUser.objects.filter(subscription=True, subscription_end_date=today)
#     for user in users:
#         user.subscription = False
#         to_emails.append(user.email)
#         user.save(update_fields=['subscription'])
    
#     #? будет отсылатся сообщение на эл. почту.
#     if to_emails:
#         return send_email(
#             header=f'| {settings.SITE_NAME} | У вас закончилась подписка',
#             msg=f'Вы можете обновить подписку на странице {subscription_link}',
#             to_emails=to_emails
#         )
#     else: return None
    
@app.task
def finish_sub(user_id, *args, **kwargs) -> None:
    #! пользователь купил подписку и через 30 дней функция сробатывает
    user = CastomUser.objects.get(pk=user_id)
    if user.subscription:
        user.subscription = False
        user.subscription_level = 0
        user.save(update_fields=['subscription', 'subscription_level'])
        send_email(
            header="У вас закончилась подписка",
            msg=f'Вы можете обновить подписку на странице {subscription_link()}',
            to_emails=[user.email]
        )
        return None
    return None


@app.task(name='clearing-old-queries')
def clearing_old_queries() -> None:
    one_month_ago = timezone.now() - timedelta(days=30)
    old_data_requests: DataPageRequest = \
        DataPageRequest.objects.filter(date_create__gte=one_month_ago.date())
    old_data_requests.delete()
    return None

@app.task
def destroy_free_sub(user_id, *args, **kwargs) -> None:
    user = CastomUser.objects.get(pk=user_id)
    user.subscription = False
    user.subscription_level = 0
    user.save()
    send_email(
            header="У вас закончилась бесплатная подписка",
            msg=f'Вы можете обновить подписку на странице {subscription_link()}',
            to_emails=[user.email]
        )
    return None