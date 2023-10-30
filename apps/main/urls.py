""" MAIN URLS """
from django.urls import path
from .views import (
    MainView, 
    get_elements, 
    save_pars_data
)


urlpatterns: list = [
    path('', MainView.as_view(), name='main'),
    path('get_elements/', get_elements, name='get_elements'),
    path('save/', save_pars_data, name='save_data')
]
