from django.urls import path
from .views import CreatePageRequests

urlpatterns: list = [
    path('page_req/', CreatePageRequests.as_view(), name='page_req'),
]