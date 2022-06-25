from django.urls import path
from . import api_views

app_name = 'kava'

urlpatterns = [
    path('', api_views.ExchangeList.as_view(), name='kava'),
]