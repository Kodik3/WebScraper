# Django.
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest
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
    
    def post(self, req: HttpRequest) -> HttpResponse:
        data = req.POST #TODO: сделать форму
        
        url = str(data.get('url')) #* ссылка.
        shift = int(data.get('shift')) #! - это шаг в секундах с которым будет выполнятся функция.
        minutes = int(data.get('duration_minutes')) #* сколько будет работать функция.
        send_email = bool(data.get('send_email')) #? отправить сообщение на почту после окончания или нет.
        file_type = str(data.get('file_type')) #* тип файла, то есть в каком виде будет записаны данные.
        
        id_name = str(data.get('id_name'))
        class_name = str(data.get('class_name'))
        
        context: dict = {}

        if req.user.is_authenticated:
            user = req.user
            if user.subscription_level == 1:
                max_minutes, min_shift, max_shift = 10, 90, 300
            elif user.subscription_level == 2:
                max_minutes, min_shift, max_shift = 30, 40, 300
            elif user.subscription_level == 3:
                max_minutes, min_shift, max_shift = 50, 20, 300
            else:
                max_minutes, min_shift, max_shift = 0, 0, 0
                return ValidationError('Неверный уровень подписки')
        else:
            max_minutes, min_shift, max_shift = 0, 0, 0
            return HttpResponseBadRequest('Вы не авторизированы')

        if minutes > max_minutes or shift < min_shift or shift > max_shift:
            return ValidationError(
                f'Подписка {user.subscription_level} lvl может делать запросы '
                f'максимум {max_minutes} минут, с задержкой не менее {min_shift} секунд и не более {max_shift} секунд'
            )
        
        page_req = PageRequests.objects.create(
            user=user,
            url=url,
            duration_minutes=minutes,
            shift=shift,
            file_type=file_type,
            send_email=send_email
        )

        if id_name != 'None':
            page_req.id_name = id_name
        if class_name != 'None':
            page_req.class_name = class_name
        page_req.save()
        
        context['page_req'] = page_req
        context['user'] = user
        work_page_request.apply_async(kwargs=context,countdown=page_req.shift)
        return HttpResponse("Success")
        