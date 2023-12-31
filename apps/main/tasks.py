import time
import eventlet
# Django.
from django.urls import reverse
# Celery.
from settings.celery import app
# models.
from auths.models import (
    PageRequests,
    DataPageRequest
)
# Local.
from .utils import GetHtml
from abstracts.utils import send_email


@app.task
def work_page_request(page_req_id: int, *args, **kwargs) -> None:
    eventlet.monkey_patch()

    start_time = int(time.time())
    objects_to_create: list = []
    duration = page_req.duration_minutes * 60

    try:
        page_req = PageRequests.objects.get(pk=page_req_id)
    except PageRequests.DoesNotExist:
        print(f"PageRequests with id {page_req_id} does not exist")

    while int(time.time()) - start_time <= duration:
        code = GetHtml.code(page_req.url)

        if page_req.class_name != 'None':
            class_elem = GetHtml.class_elements(code, page_req.class_name, page_req.content_type)
            objects_to_create.append(DataPageRequest(user=page_req.user, data=class_elem, content_type=page_req.content_type))

        if page_req.id_name != 'None':
            id_elem = GetHtml.id_elements(code, page_req.id_name, page_req.content_type)
            objects_to_create.append(DataPageRequest(user=page_req.user, data=id_elem, content_type=page_req.content_type))

        time.sleep(int(page_req.shift))

    DataPageRequest.objects.bulk_create(objects_to_create, batch_size=len(objects_to_create))
    print('DataPageRequest is created!')

    if page_req.send_email:
        user_profile_url = reverse('user_profile')
        user_profile_link = f'<a href="{user_profile_url}">кабинет</a>'
        
        send_email(
            header=f"Работа завершена!",
            msg=f"Ваши запросы завершились. Зайдите в свой {user_profile_link}, чтобы проверить.",
            to_emails=[page_req.user.email,]
        )
    return None
