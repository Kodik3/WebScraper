# Django.
from django.http import (
    HttpRequest,
    HttpResponse
)
from django.shortcuts import render
from django import views
from django.core.exceptions import ValidationError
# models.
from .models import CastomUser, PageRequests
from .tasks import work_page_request

class CreatePageRequests(views.View):
    def get(self, req:HttpRequest) -> HttpResponse:
        ...
    
    def post(self, req:HttpRequest) -> HttpResponse:
        data = req.POST #TODO: сделать форму
        user = req.user
        
        url = str(data.get('url'))
        shift = int(data.get('shift')) # задержка в секундах.
        minutes = int(data.get('duration_minutes'))
        send_email = bool(data.get('send_email'))
        
        id_name = str(data.get('id_name'))
        class_name = str(data.get('class_name'))
        
        context: dict = {}
        
        if user.subscription_level == 1: #! max_min: 10, max_shift: 1:30 min (90 sec)
            if minutes <= 10 and shift >= 90:
                page_req = PageRequests.objects.create(
                    user=user,
                    url=url,
                    duration_minutes=minutes,
                    shift=shift,
                    send_email=send_email
                )
                if id_name != 'None':
                    page_req.id_name = id_name
                if class_name != 'None':
                    page_req.class_name = class_name
                page_req.save()
                work_page_request.apply_async(kwargs=context,countdown=page_req.shift)
            else:
                return ValidationError('Подписка 1 lvl может делать запросы максимум 10 минут')

        elif user.subscription_level == 2: #! max_min: 30, max_shift: 40 sec
            if minutes <= 30 and shift >= 40:
                page_req = PageRequests.objects.create(
                    user=user,
                    url=url,
                    shift=shift,
                    send_email=send_email
                )
                if id_name != 'None':
                    page_req.id_name = id_name
                if class_name != 'None':
                    page_req.class_name = class_name
                page_req.save()
                work_page_request.apply_async(kwargs=context,countdown=page_req.shift)
            else:
                return ValidationError('Подписка 2 lvl может делать запросы максимум 30 минут')
                
        elif user.subscription_level == 3: #! max_min: 50, max_shift: 20 sec
            if minutes <= 50 and shift >= 20:
                page_req = PageRequests.objects.create(
                    user=user,
                    url=url,
                    shift=shift,
                    send_email=send_email
                )
                if id_name != 'None':
                    page_req.id_name = id_name
                if class_name != 'None':
                    page_req.class_name = class_name
                page_req.save()
                work_page_request.apply_async(kwargs=context,countdown=page_req.shift)
            else:
                return ValidationError('Подписка 3 lvl может делать запросы максимум 50 минут')
        else: return None
        