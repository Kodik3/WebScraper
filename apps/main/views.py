# Python.
import random
import json
# Django.
from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.core.files.base import ContentFile
# Local.
from .forms import MainForm
from .utils import GetHtml
# models.
from .models import (
    JsonElement,
    TextElement
)

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
            url = str(form.cleaned_data['url'])
            code = GetHtml.code(url) # HTML code.
            if code is not None:
                ids = GetHtml.all_id(code)# id.
                classes = GetHtml.all_class(code) # class.

                context['ids'] = ids
                context['classes'] = classes

            context['uurl'] = url
        context['form'] = form
        return render(req, self.template, context)


def get_elements(req: HttpRequest) -> HttpResponse:
    """ получение данных из тегов id и class """
    context: dict = {}
    try:
        data = req.POST
        url = data.get('uurl')
        
        selected_id = data.get('selected_id') #* id
        selected_class = data.get('selected_class') #* class

        #! RANGE:
        first_range: int = int(data.get('from'))
        last_range: int = int(data.get('to'))
        if last_range > 0:
            try:
                pages = GetHtml.multiple_pages(
                    url=url,
                    range_=[first_range, last_range],
                    class_name=selected_class,
                    id_name=selected_id
                )
            except Exception as e:
                context['error'] = str(e)
            context['classes'] = pages.get('classes')
            context['ids'] = pages.get('ids')
            print(context)
            return render(req, 'result_data.html', context)
            
        if selected_class is not None:
            context['classes']  = GetHtml.class_elements(
                code=GetHtml.code(url=url),
                class_name=selected_class
            )
        if selected_id is not None:
            context['ids']  = GetHtml.id_elements(
                code=GetHtml.code(url=url),
                id_name=selected_id
            )
    except Exception as e:
        context['error'] = str(e)
    return render(req, 'result_data.html', context)


def save_pars_data(req: HttpRequest) -> HttpResponse:
    """ сохронения данных """
    if req.method == 'POST':
        data = req.POST
        result_data = data.get('result_data')
        content_type = data.get('content_type')

        try:
            if content_type == 'json':
                element = JsonElement.objects.create(
                    name=f"noname{random.randint(0, 1000)}",
                )
                element.name = f"pars_document{element.id}.{content_type}"
                content_file = ContentFile(result_data)
                element.file.save(element.name, content_file)
                element.save()
                return redirect(element.file.url)

            if content_type == 'txt':
                result_data = json.loads(result_data)
                text = ''.join(
                    "{}. {}\n".format(idx, list(elem.values())[0]) for idx, elem in enumerate(result_data, 1)
                )
                element = TextElement.objects.create(
                    name=f"noname{random.randint(0, 1000)}",
                )
                element.name = f"pars_document{element.id}.txt"
                content_file = ContentFile(text)
                element.file.save(element.name, content_file)
                element.save()
                return redirect(element.file.url)

        except Exception as e:
            return HttpResponse(f"Error: {e}")