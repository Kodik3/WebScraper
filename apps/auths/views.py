
"""| AUTHS VIEWS |"""

from django.http import (
    HttpRequest,
    HttpResponse,
    Http404
)
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
# model.
from .models import DataPageRequest, CastomUser
# forms.
from .forms import RegisterUserForm, LoginUserForm
# tasks
from .tasks import destroy_free_sub
# Local.
from abstracts.utils import send_email


class RegistrationView(View):
    template: str = 'registration.html'

    def get(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        context['form'] = RegisterUserForm()
        return render(req, self.template, context)

    def post(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        form = RegisterUserForm(req.POST)

        if form.is_valid():
            del form.cleaned_data['password2']
            user = CastomUser.objects.create(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(req, user)
            return redirect('user_profile')
        
        context['form'] = form
        return render(req, self.template, context)


class LoginView(View):
    template: str = 'login.html'

    def get(self, req: HttpRequest) -> HttpResponse:
        user = req.user
        if user.is_authenticated:
            return HttpResponse('Вы уже авторизованы!')
        context: dict = {}
        context['form'] = LoginUserForm()
        return render(req, self.template, context)

    def post(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        form = LoginUserForm(req.POST)
        if form.is_valid():
            email = str(form.cleaned_data['email'])
            password = str(form.cleaned_data['password'])
            user = authenticate(req, email=email, password=password)
            if user is not None:
                login(req, user)
                return redirect('user_profile')
            else:
                return Http404
        context['form'] = form
        return render(req, self.template, context)


class UserProfile(View):
    template: str = 'user_profile.html'

    def get(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        user = req.user
        if not user.is_authenticated:
            return redirect('login')
        context['user'] = user
        return render(req, self.template, context)


class AllUserPagesRequestsView(View):
    template: str = 'all_user_req_page.html'
    OBJECTS_PER_PAGE: int = 10 #* Количество объектов на одной странице

    def get(self, req: HttpRequest) -> HttpResponse:
        user = req.user
        if not user.is_authenticated:
            return HttpResponse("У вас нет аккаунта. Создайте аккаунт, чтобы использовать эту функцию.")

        context: dict = {}
        content_type = req.GET.get('content_type')
        objects = DataPageRequest.objects.filter(user=user)

        if content_type:
            objects = objects.filter(content_type=content_type)

        paginator = Paginator(objects, self.OBJECTS_PER_PAGE)

        page = req.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context['current_page'] = current_page
        return render(req, self.template, context)


class BuySubView(View):
    template: str = 'purchasing_sub.html'
    def get(self, req: HttpRequest) -> HttpResponse:
        context: dict = {}
        return render(req, self.template, context)


def user_logout(req: HttpRequest):
    """
    функция выхода пользователя из сессии.
    """
    logout(req)
    return redirect('login')


def free_sub(req: HttpRequest) -> HttpResponse:
    context: dict = {}
    user = req.user
    DAYS_ACTIVE_3  = 3*24*60*60
    if user.is_authenticated:
        if user.free_subscription_is_use == True:
            return HttpResponse("Вы использовали бесплатную подписку!")
        user.free_subscription_is_use = True
        user.subscription = True
        user.subscription_level = 1
        user.save()

        context['user'] = user
        destroy_free_sub.apply_async(kwargs=context, countdown=DAYS_ACTIVE_3)
        send_email(
            header=f"| {settings.SITE_NAME} | Подписка lvl-1",
            msg='Вы получили подписку, она закончится через 3 дня',
            to_emails=[user.email]
        )
        return redirect('main')
    else:
        return HttpResponse("Нужно войти в аккаунт")


def detail_data_requests(req: HttpRequest, item_id: int) -> HttpResponse:
    context: dict = {}
    try:
        data_req_item = DataPageRequest.objects.get(pk=item_id)
    except DataPageRequest.DoesNotExist as e:
        raise Http404(e)

    context['data_req_item'] = data_req_item
    return render(req, 'detail_data_req.html', context)

def save_page_request_data(req: HttpRequest, item_id: int) -> HttpResponse:
    page_data: DataPageRequest = DataPageRequest.objects.get(pk=item_id)
    page_data.name = f"page_data{item_id}.{page_data.content_type}"

    content_bytes = page_data.data.encode('utf-8') # Закодируйте строку в байты перед созданием
    content_file = ContentFile(content_bytes)
    page_data.file.save(page_data.name, content_file)
    page_data.save()

    response = HttpResponse(page_data.file.read(), content_type=page_data.content_type)
    response["Content-Disposition"] = f'attachment; filename="{page_data.name}"'
    return response