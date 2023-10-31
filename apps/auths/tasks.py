# Python.
from datetime import datetime as dt
import time
# models.
from .models import CastomUser, DataPageRequest
# Celery.
from settings.celery import app
from celery import shared_task
# requests.
from main.utils import GetHtml
from .models import PageRequests


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
    duration = page_req.duration_minutes * 60
    start_time = time.time()

    qty: int = 1 #* количество сробатываний функции.
    result_data: dict = {}

    while time.time() - start_time <= duration:
        code = GetHtml.code(page_req.url)
        data = []

        class_elem = GetHtml.class_elements(code, page_req.class_name)
        id_elem = GetHtml.id_elements(code, page_req.id_name)

        result_data = class_elem + id_elem

        if page_req.file_type == 'json':
            data.append({"class" : class_elem, "id" : id_elem})
        if page_req.file_type == 'txt':
            text = ''.join(
                    "{}. {}\n".format(idx, list(elem.values())[0]) for idx, elem in enumerate(result_data, 1)
                )
        return result_data

# data = {
#             'url': 'https://quotes.toscrape.com/',
#             'shift': 20,
#             'duration_minutes': 5,
#             'send_email': False,
#             'file_type': 'json',
#             'id_name': 'None',
#             'class_name': 'quote',
#         }
# user = CastomUser.objects.get(id=1)
# fake_page_req = PageRequests.objects.create(
#     user=user,
#     url=data['url'],
#     shift=data['shift'],
#     duration_minutes=data['duration_minutes'],
#     send_email=data['send_email'],
#     file_type=data['file_type'],
#     id_name=data['id_name'],
#     class_name=data['class_name'],
# )

# @shared_task
# def test_page_req():
#     result = work_page_request.apply_async(args=[fake_page_req])
#     print("Task ID:", result.id)
#     print("MY RESULT: ", result)