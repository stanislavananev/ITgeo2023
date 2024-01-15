from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserPortfolio


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ExchangeForm(forms.Form):
    amount = forms.DecimalField()
    currency = forms.ChoiceField(choices=[('eur', 'EUR'), ('gbp', 'GBP'), ('jpy', 'JPY')])
    action = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])


class UserAddForm(forms.ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ['user', 'usd_balance', 'eur_balance', 'gbp_balance', 'jpy_balance']