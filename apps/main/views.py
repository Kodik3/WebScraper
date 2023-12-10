
"""| MAIN VIEWS |"""

# Django.
from django.http import (
    HttpRequest,
    HttpResponse
)
from django.shortcuts import render
from django.views import View
from django.core.files.base import ContentFile
# Local.
from .utils import (
    GetHtml,
    MultiplePages
)
from .tasks import work_page_request
# models.
from .models import Element
from auths.models import PageRequests
from subscription.models import Subscription


class MainView(View):
    template: str = 'main_template.html'

    def get(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        context['user'] = req.user
        return render(req, self.template, context)

    def post(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        url = req.POST.get('url')
        code = GetHtml.code(str(url))
        context["uurl"] = str(url)
        ids = GetHtml.all_id(code)
        classes = GetHtml.all_class(code)

        context["ids"] = ids
        context["classes"] = classes
        return render(req, self.template, context)


class CreatePageRequests(View):
    template: str = 'temporary_page_request.html'

    def get(self, req:HttpRequest) -> HttpResponse:
        user = req.user
        if not user.is_authenticated:
            return HttpResponse('Вы не авторизированы')
        elif user.subscription is not True:
            return HttpResponse('У вас не подписки')
        context: dict = {}
        context["content_types"] = ['json', 'txt']
        return render(req, self.template, context)
    
    def post(self, req: HttpRequest) -> HttpResponse:
        data = req.POST
        user = req.user
        
        url = str(data.get('url')) #* ссылка.
        shift = int(data.get('shift')) #? - это шаг в секундах с которым будет выполнятся функция.
        minutes = int(data.get('duration_minutes')) #* сколько времени будет работать функция.
        send_email = bool(data.get('send_email', False) == 'on') #! отправить сообщение на почту после окончания или нет.
        content_type = str(data.get('content_type')) #* тип файла, то есть в каком виде будет записаны данные.
        
        id_name = str(data.get('id_name'))
        class_name = str(data.get('class_name'))

        context: dict = {}

        if id_name == 'None' and class_name == 'None':
            context['url'] = url
            context['shift'] = shift
            context['minutes'] = minutes
            context["content_types"] = ['json', 'txt']
            context['elements_error'] = "Нужно выбрать элементы для создания запроса!"
            return render(req, self.template, context)
        
        user_settings: dict = Subscription.objects.get(level=user.subscription_level).settings()

        if minutes > user_settings['max_minutes']\
        or shift < user_settings['min_shift']\
        or shift > user_settings['max_shift']:
            return HttpResponse(f"""
                Подписка {user.subscription_level} lvl может делать запросы
                максимум {user_settings['max_minutes']} минут, 
                с задержкой не менее {user_settings['min_shift']} секунд 
                и не более {user_settings['max_shift']} секунд
                """)

        page_req = PageRequests(
            user=user,
            url=url,
            duration_minutes=minutes,
            shift=shift,
            content_type=content_type,
            send_email=send_email,
            id_name=id_name,
            class_name=class_name
        )
        page_req.save()
        context['page_req_id'] = page_req.id
        work_page_request.apply_async(kwargs=context)
        return HttpResponse("Success")


def get_elements(req: HttpRequest) -> HttpResponse:
    """ получение данных из тегов id и class """
    context: dict = {}
    try:
        data = req.POST
        url = data.get('uurl')
        # class, id
        selected_id = str(data.get('selected_id'))
        selected_class = str(data.get('selected_class'))
        # type, range
        content_type = str(data.get('content_type'))
        is_range: str = str(data.get('is_range'))
        
        if is_range == 'True':
            first_range: int = int(data.get('from'))
            last_range: int = int(data.get('to'))
            try:
                if content_type == 'json':
                    pages = MultiplePages.get_json_data(
                        url=url,
                        page_range=[first_range, last_range],
                        cls_name=selected_class,
                        id_name=selected_id
                    )
                    context["content_type"] = content_type
                elif content_type == 'txt':
                    pages = MultiplePages.get_text_data(
                        url=url,
                        page_range=[first_range, last_range],
                        cls_name=selected_class,
                        id_name=selected_id
                    )
                    context["content_type"] = content_type
                else:
                    print("[Error] MultiplePages")
                print("MultiplePages")
                print(pages)
                context["pages"] = pages
            except Exception as e:
                context["error"] = str(e)
        else:
            if selected_class != 'None':
                context["classes"] = GetHtml.class_elements(
                    code=GetHtml.code(url=url),
                    class_name=selected_class,
                    content_type=content_type
                )
                context["content_type"] = content_type
                print("selected_class")
            if selected_id != 'None':
                context["ids"] = GetHtml.id_elements(
                    code=GetHtml.code(url=url),
                    id_name=selected_id,
                    content_type=content_type
                )
                context["content_type"] = content_type
                print("selected_id")
    except Exception as e:
        context["error"] = str(e)
    return render(req, 'result_data.html', context)

def save_pars_data(req: HttpRequest) -> HttpResponse:
    """
    Функция сохроняет данные на ПК пользователя.
    """
    if req.method == 'POST':
        data = req.POST
        result_data = data.get('result_data')
        content_type = data.get('content_type')
        
        element: Element = Element.objects.create()
        element.name = f"pars_document{element.id}.{content_type}"
        content_file = ContentFile(result_data)
        element.file.save(element.name, content_file)
        element.save()
        
        response = HttpResponse(element.file.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{element.name}"'
        return response

def page_req_get_elements(req: HttpRequest) -> HttpResponse:
    context: dict = {}
    url = req.POST.get('url')
    code = GetHtml.code(url)
    context["content_types"] = ['json', 'txt']
    context["url"] = url
    context["id_names"] = GetHtml.all_id(code)
    context["class_names"] = GetHtml.all_class(code)
    return render(req, 'temporary_page_request.html', context)
