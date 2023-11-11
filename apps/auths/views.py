from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# model.
from .models import DataPageRequest


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