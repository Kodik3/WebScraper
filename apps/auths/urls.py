
"""| AUTHS URLS |"""

from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    UserProfile,
    AllUserPagesRequestsView,
    BuySubPageView,
    user_logout,
    free_sub,
    detail_data_requests,
    save_page_request_data
)

urlpatterns: list = [
    path('reg/', RegistrationView.as_view(), name='registration'),
    path('log/', LoginView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('logout/', user_logout, name='logout'),

    path('request_data/', AllUserPagesRequestsView.as_view(), name='req_data'),
    path('detail_data_req/<int:item_id>/', detail_data_requests, name='detail_data_req'),
    path('detail_data_req/<int:item_id>/save',save_page_request_data, name='save_page_data'),

    path('sub/', BuySubPageView.as_view(), name='buy_sub'),
    # path('sub/<int:sub_lvl>'),#!!!!!!!!!!!!!!!!
    path('free/sub/', free_sub, name='free_sub')
]