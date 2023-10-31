from django.urls import path
from . import views
from .views import get_currency_data, list_currencies

urlpatterns = [
    path('', views.index, name='index'),
    path('api/currencies/', list_currencies, name='list_currencies'),
    path('api/currency_data/<str:currency_code>/', get_currency_data, name='get_currency_data'),
]
