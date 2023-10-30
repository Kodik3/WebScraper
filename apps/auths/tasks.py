# Python.
from datetime import datetime as dt
# models.
from .models import CastomUser
# Celery.
from settings.celery import app
import schedule
# requests.
from main.utils import GetHtml
# from abstracts.utils import send_email


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
    # if to_emails:
    #     return send_email(
    #         'У вас закончилась подписка',
    #         'обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки'),
    #         to_emails
    #     )
    # else: return None
    
@app.task
def finish_sub(sub, *args, **kwargs):
    #! будет запускатся когда
    #! пользователь купил подписку
    #! и через 30 дней функция сробатывает
    sub.is_active = False
    sub.save(update_fields=['is_active'])
    print("Sub finish")
    
@app.task
def work_page_request(page_req, *args, **kwargs):
    code = GetHtml.code(page_req.url)
    class_elem = GetHtml.class_elements(code, page_req.class_name)
    id_elem = GetHtml.id_elements(code, page_req.id_name)
