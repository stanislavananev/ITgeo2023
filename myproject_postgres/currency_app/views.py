from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Currency, HistoricalExchangeRate, UserPortfolio
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ExchangeForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from influxdb_client import InfluxDBClient
import pytz


def default(request):
    return render(request, 'currency_app/apps_link.html')


def homepage(request):
    return render(request, 'currency_app/homepage.html')


def rates_page(request):
    if request.user.is_authenticated:
        return render(request, 'currency_app/exchange_rates.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return redirect('login')


def admin_page(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        user_profiles = UserPortfolio.objects.all()

        return render(request, 'currency_app/admin_page.html', {'user_profiles': user_profiles})
    else:
        messages.error(request, 'You need to be admin to see this page')
        return redirect('login')


def account_view(request):
    if request.user.is_authenticated:
        messages.get_messages(request).used = True
        try:
            user_portfolio = UserPortfolio.objects.get(user=request.user)
        except ObjectDoesNotExist:
            user_portfolio = UserPortfolio.objects.create(user=request.user)
        user_portfolio.save()
        if request.method == 'POST':
            form = ExchangeForm(request.POST)
            if form.is_valid():
                user_portfolio = UserPortfolio.objects.get(user=request.user)
                amount = form.cleaned_data['amount']
                currency_name = form.cleaned_data['currency'].upper()
                action = form.cleaned_data['action']

                code = get_object_or_404(Currency, code=currency_name)
                currency = HistoricalExchangeRate.objects.filter(currency=code).order_by('timestamp')
                currency = currency[::-1]
                currency_value = currency[0].exchange_rate

                if action == 'buy':
                    if currency_name == 'EUR':
                        user_portfolio.eur_balance += amount
                        user_portfolio.usd_balance -= amount/currency_value
                    if currency_name == 'GBP':
                        user_portfolio.gbp_balance += amount
                        user_portfolio.usd_balance -= amount/currency_value
                    if currency_name == 'JPY':
                        user_portfolio.jpy_balance += amount
                        user_portfolio.usd_balance -= amount/currency_value
                else:
                    if currency_name == 'EUR':
                        user_portfolio.eur_balance -= amount
                        user_portfolio.usd_balance += amount/currency_value
                    if currency_name == 'GBP':
                        user_portfolio.gbp_balance -= amount
                        user_portfolio.usd_balance += amount/currency_value
                    if currency_name == 'JPY':
                        user_portfolio.jpy_balance -= amount
                        user_portfolio.usd_balance += amount/currency_value

                if user_portfolio.usd_balance >= 0 and user_portfolio.eur_balance >= 0 and user_portfolio.gbp_balance >= 0 and user_portfolio.jpy_balance >= 0:
                    user_portfolio.save()
                else:
                    messages.error(request, "Sorry, you don't have enough currency.")
                return redirect('/currency_app/profile')
        else:
            form = ExchangeForm()

        return render(request, 'currency_app/profile.html', {'user_portfolio': user_portfolio, 'form': form})
    else:
        messages.error(request, 'You need to be logged in to access this page.')
        return redirect('login')


def custom_logout(request):
    logout(request)
    return redirect('login')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/currency_app/exchange_rates')
    messages_to_display = messages.get_messages(request)
    return render(request, 'currency_app/login.html',  {'messages_to_display': messages_to_display})


def signup_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/currency_app')
    else:
        form = CreateUserForm()

    return render(request, 'currency_app/signup.html', {'form': form})


def list_currencies(request):
    currencies = Currency.objects.all().order_by('code')
    currency_codes = [currency.code for currency in currencies]
    return JsonResponse({'currencies': currency_codes})


def get_currency_data(request, currency_code):
    currency = get_object_or_404(Currency, code=currency_code)
    data = HistoricalExchangeRate.objects.filter(currency=currency).order_by('timestamp')
    data = data[::-1]
    response_data = {
        'labels': [str(item.timestamp) for item in data],
        'datasets': [{
            'label': currency_code,
            'data': [float(item.exchange_rate) for item in data],
        }]
    }

    return JsonResponse(response_data)


@login_required
def update_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        field_type = request.POST.get('field')
        value = request.POST.get('new_value')
        try:
            user_portfolio = UserPortfolio.objects.get(user_id=user_id)
            if field_type == 'username':
                user.username = value
                user.save()
            if field_type == 'usd':
                user_portfolio.usd_balance = value
            if field_type == 'usd':
                user_portfolio.usd_balance = value
            if field_type == 'eur':
                user_portfolio.eur_balance = value
            if field_type == 'gbp':
                user_portfolio.gbp_balance = value
            if field_type == 'jpy':
                user_portfolio.jpy_balance = value
            user_portfolio.save()
            return HttpResponse('Balance updated successfully', status=200)
        except UserPortfolio.DoesNotExist:
            return HttpResponse('User not found', status=404)
    return HttpResponse('Invalid request', status=400)


@login_required
def delete_user_portfolio(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            # user_portfolio = UserPortfolio.objects.get(user_id=user_id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'User portfolio deleted'})
        except UserPortfolio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User portfolio not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def add_user_portfolio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        usd_balance = request.POST.get('usd_balance')
        eur_balance = request.POST.get('eur_balance')
        gbp_balance = request.POST.get('gbp_balance')
        jpy_balance = request.POST.get('jpy_balance')

        try:
            user, created = User.objects.get_or_create(username=username)
            user_portfolio = UserPortfolio.objects.create(
                user=user,
                usd_balance=usd_balance,
                eur_balance=eur_balance,
                gbp_balance=gbp_balance,
                jpy_balance=jpy_balance,
            )
            user_portfolio.save()
            return JsonResponse({'status': 'success', 'message': 'User portfolio added', 'new_user_id': user_portfolio.user.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
