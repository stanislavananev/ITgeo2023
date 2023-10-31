from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Currency, HistoricalExchangeRate


def index(request):
    return render(request, 'currency_app/index.html')


def list_currencies(request):
    currencies = Currency.objects.all()
    currency_codes = [currency.code for currency in currencies]
    return JsonResponse({'currencies': currency_codes})


def get_currency_data(request, currency_code):
    currency = get_object_or_404(Currency, code=currency_code)
    data = HistoricalExchangeRate.objects.filter(currency=currency).order_by('timestamp')

    response_data = {
        'labels': [str(item.timestamp) for item in data],
        'datasets': [{
            'label': currency_code,
            'data': [float(item.exchange_rate) for item in data],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }

    return JsonResponse(response_data)



