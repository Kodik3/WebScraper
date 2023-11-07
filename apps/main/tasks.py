# Python.
from datetime import datetime as dt
import time
# Django.
from django.conf import settings
# Celery.
from settings.celery import app
# models.
from auths.models import (
    CastomUser, 
    DataPageRequest
)
# Local.
from .utils import GetHtml
from abstracts.utils import send_email


@app.task
def work_page_request(page_req, *args, **kwargs):
    objects_to_create: list = []

    duration = page_req.duration_minutes * 60
    start_time = time.time()
    
    while time.time() - start_time <= duration:
        code = GetHtml.code(page_req.url)

        if page_req.class_name != 'None':
            class_elem = GetHtml.class_elements(code, page_req.class_name, page_req.content_type)
            objects_to_create.append(DataPageRequest(user=page_req.user, data= class_elem))

        if page_req.id_name != 'None':
            id_elem = GetHtml.id_elements(code, page_req.id_name, page_req.content_type)
            objects_to_create.append(DataPageRequest(user=page_req.user, data=id_elem))

        time.sleep(page_req.shift)

    DataPageRequest.objects.bulk_create(objects_to_create, batch_size=len(objects_to_create))
    if page_req.send_email:
        send_email(
            header=f"| {settings.SITE_NAME} | Работа завершена!",
            msg="Ваши запросы завершились. Зайдите в свой <a href="">кабинет</a>, чтобы проверить.",
            to_emails=[page_req.user.email,]
        )
