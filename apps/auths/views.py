
"""| AUTHS VIEWS |"""

from django.http import (
    HttpRequest,
    HttpResponse,
    Http404
)
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
# model.
from .models import DataPageRequest, CastomUser
# forms.
from .forms import RegisterUserForm, LoginUserForm


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

    def get(self, req: HttpRequest) -> HttpResponse:

        user = req.user
        if not user.is_authenticated:
            return HttpResponse("У вас нет аккаунта. Создайте аккаунт, чтобы использовать эту функцию.")

        context: dict = {}
        OBJECTS_PER_PAGE: int = 10 #* Количество объектов на одной странице

        objects = DataPageRequest.objects.filter(user=user)
        paginator = Paginator(objects, OBJECTS_PER_PAGE)

        page = req.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context['current_page'] = current_page
        return render(req, self.template, context)

class SubDocumentation(View):
    """
    Template c документацией о уровнях подписки.
    """
    template: str = 'sub_documentation.html'
    def get(self, req: HttpRequest) -> HttpResponse:
        return render(req, self.template)


def user_logout(req: HttpRequest):
    logout(req)
    return redirect('login')
