
"""| AUTHS URLS |"""

from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    UserProfile,
    AllUserPagesRequestsView,
    SubDocumentation,
    user_logout
)

urlpatterns: list = [
    path('reg/', RegistrationView.as_view(), name='registration'),
    path('log/', LoginView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('logout/', user_logout, name='logout'),
    path('request_data/', AllUserPagesRequestsView.as_view(), name='req_data'),
    path('sub_doc/', SubDocumentation.as_view(), name='sub_doc')
]