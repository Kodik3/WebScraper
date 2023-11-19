""" MAIN URLS """
from django.urls import path
from .views import (
    MainView,
    CreatePageRequests,
    get_elements, 
    save_pars_data,
    page_req_get_elements,
)


urlpatterns: list = [
    path('', MainView.as_view(), name='main'),
    path('elements/', get_elements, name='get_elements'),
    path('elements/save/', save_pars_data, name='save_data'),
    path('create/page_req/', CreatePageRequests.as_view(), name='page_req'),
    path('create/page_req/elem/', page_req_get_elements, name='page_req_elem'),
]