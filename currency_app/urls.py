from django.urls import path, include
from . import views
from .views import get_currency_data, list_currencies, custom_logout


urlpatterns = [
    path('', views.default, name='apps_list'),
    path('currency_app/', views.homepage, name='homepage'),
    path('currency_app/exchange_rates', views.rates_page, name='exchange_rates'),
    path('currency_app/login', views.login_page, name='login'),
    path('currency_app/signup', views.signup_page, name='signup'),
    path('currency_app/profile', views.account_view, name='user_profile'),
    path('currency_app/admin_page', views.admin_page, name='admin_page'),
    path('logout/', custom_logout, name='logout'),
    path('currency_app/api/currencies/', list_currencies, name='list_currencies'),
    path('currency_app/api/currency_data/<str:currency_code>/', get_currency_data, name='get_currency_data'),
    path('currency_app/api/update_info/', views.update_info, name='update_info'),
    path('currency_app/api/delete_user_portfolio/', views.delete_user_portfolio, name='delete_user_portfolio'),
    path('currency_app/api/add_user_portfolio/', views.add_user_portfolio, name='add_user_portfolio'),
]
