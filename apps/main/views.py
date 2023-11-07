# Django.
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest
)
from django.shortcuts import render, redirect
from django.views import View
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
# Local.
from .forms import MainForm
from .utils import GetHtml, MultiplePages
from .tasks import work_page_request
# models.
from .models import Element
from auths.models import CastomUser, PageRequests

#! Главная страница.
class MainView(View):
    """ для полученяи кода страницы """
    template: str = 'main_page.html'

    def get(self, req: HttpRequest) -> HttpResponse:
        form = MainForm()
        context: dict = {}
        context['form'] = form
        return render(req, self.template, context)

    def post(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        form = MainForm(data=req.POST)
        if form.is_valid():
            code = GetHtml.code(str(form.cleaned_data['url'])) # HTML code.
            context["uurl"] = str(form.cleaned_data['url'])

            if code is not None:
                ids = GetHtml.all_id(code) # id.
                classes = GetHtml.all_class(code) # class.

                context["ids"] = ids
                context["classes"] = classes
        context["form"] = form
        return render(req, self.template, context)


class CreatePageRequests(View):
    template: str = 'temporary_page_request.html'

    def get(self, req:HttpRequest) -> HttpResponse:
        context: dict = {}
        context["content_types"] = ['json', 'txt'] #! сделать удобнее!
        return render(req, self.template, context)
    
    def post(self, req: HttpRequest) -> HttpResponse:
        data = req.POST
        
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
            context['elements_error'] = "Нужно выбрать элементы для создания запроса!"
            return render(req, self.template, context)

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
                f"""
                Подписка {user.subscription_level} lvl может делать запросы '
                максимум {max_minutes} минут, с задержкой не менее {min_shift} секунд и не более {max_shift} секунд
                """
            )
        page_req: PageRequests = \
            PageRequests.objects.create(
            user=user,
            url=url,
            duration_minutes=minutes,
            shift=shift,
            content_type=content_type,
            send_email=send_email,
            id_name=id_name,
            class_name=class_name
        )
        context['page_req'] = page_req
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
    """ сохранение данных """
    if req.method == 'POST':
        data = req.POST
        result_data = data.get('result_data')
        content_type = data.get('content_type')
        print(f"Content Type: {content_type}")

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
    context["url"] = url
    context["id_names"] = GetHtml.all_id(code)
    context["class_names"] = GetHtml.all_class(code)
    return render(req, 'temporary_page_request.html', context)
