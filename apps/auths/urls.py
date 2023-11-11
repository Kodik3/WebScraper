from django.urls import path
from .views import (
    AllUserPagesRequestsView
)

urlpatterns: list = [
    path('request_data/', AllUserPagesRequestsView.as_view(), name='req_data'),
]