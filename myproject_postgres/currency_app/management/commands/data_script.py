from django.core.management.base import BaseCommand
import random
import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from currency_app.models import Currency, HistoricalExchangeRate
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Fetches data and updates the model periodically'

    def handle(self, *args, **options):
        while True:
            exchange_rate_data = fetch_exchange_rates()
            update_exchange_rates(exchange_rate_data)
            time.sleep(120 + random.randint(-15, 15))


def parse_labels():
    cookies = {
        'f5_cspm': '1234',
        'TS1d092b86029': '08e458c34fab280006ef6271e7d2493d6a17f4c38c822dcee13246fdeecfdab7324f3381b850e10f9fe4bd3683970d2b',
        'EMGEO2': '94.180.118.183:RU:Russia:syc:Asia/Novosibirsk',
        'OFFICEIP': '',
        'TS017f483b': '0171abe9cb9f24adc5db124407a0379923abb9639861618e52c918f97189c2bb8bc5558f4c9f7c9760d5076bbce2fd8539edd7eee4d8c773e0739afaabd883a80aa4c8d025b233b53c5a35aa9978a8619d069bdcffecea6b8f25d591bca7d23897883d5a4adebdcc104e9a6903d7a2ee3b830e0e99',
        '_fbp': 'fb.1.1696933122285.969608035',
        '_ga': 'GA1.2.1860631665.1696933121',
        '_ga_DZQ80SS4CB': 'GS1.1.1696933121.1.0.1696933121.60.0.0',
        '_gid': 'GA1.2.1643683552.1696933121',
        '_tt_enable_cookie': '1',
        '_ttp': '6iskPHfcnNMexPLookKdxumCRvd',
        'ln_or': 'eyIxMzk2NTA2LDUwNjY3NTMiOiJkIn0%3D',
        '_gcl_au': '1.1.1866978699.1696933121',
        'auth': '%7B%22sessionId%22%3A%223675_3d10aa5f-7d34-4198-833d-aaf2592e2bc5%22%2C%22isAuthenticated%22%3Afalse%7D',
        'cookieConsent': '%7B%22functional%22%3Atrue%2C%22performance%22%3Atrue%2C%22behavioural%22%3Atrue%7D',
        'cookieConsentDate': '2023-10-10T10%3A18%3A40',
        'de4fe6': 'TAR%3D6279967%26JAR%3D0',
        'gtw_id': '6279967',
        'referer': 'https%3A%2F%2Fwww.google.com%2F',
        'siteLanguage': 'en',
        'url_lang': 'en',
        'utm_params': '%7B%22utm_source%22%3A%22Google%22%2C%22utm_medium%22%3A%22serp%22%2C%22utm_ef_channel%22%3A%22Organic%22%7D',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        # 'Cookie': 'f5_cspm=1234; TS1d092b86029=08e458c34fab280006ef6271e7d2493d6a17f4c38c822dcee13246fdeecfdab7324f3381b850e10f9fe4bd3683970d2b; EMGEO2=94.180.118.183:RU:Russia:syc:Asia/Novosibirsk; OFFICEIP=; TS017f483b=0171abe9cb9f24adc5db124407a0379923abb9639861618e52c918f97189c2bb8bc5558f4c9f7c9760d5076bbce2fd8539edd7eee4d8c773e0739afaabd883a80aa4c8d025b233b53c5a35aa9978a8619d069bdcffecea6b8f25d591bca7d23897883d5a4adebdcc104e9a6903d7a2ee3b830e0e99; _fbp=fb.1.1696933122285.969608035; _ga=GA1.2.1860631665.1696933121; _ga_DZQ80SS4CB=GS1.1.1696933121.1.0.1696933121.60.0.0; _gid=GA1.2.1643683552.1696933121; _tt_enable_cookie=1; _ttp=6iskPHfcnNMexPLookKdxumCRvd; ln_or=eyIxMzk2NTA2LDUwNjY3NTMiOiJkIn0%3D; _gcl_au=1.1.1866978699.1696933121; auth=%7B%22sessionId%22%3A%223675_3d10aa5f-7d34-4198-833d-aaf2592e2bc5%22%2C%22isAuthenticated%22%3Afalse%7D; cookieConsent=%7B%22functional%22%3Atrue%2C%22performance%22%3Atrue%2C%22behavioural%22%3Atrue%7D; cookieConsentDate=2023-10-10T10%3A18%3A40; de4fe6=TAR%3D6279967%26JAR%3D0; gtw_id=6279967; referer=https%3A%2F%2Fwww.google.com%2F; siteLanguage=en; url_lang=en; utm_params=%7B%22utm_source%22%3A%22Google%22%2C%22utm_medium%22%3A%22serp%22%2C%22utm_ef_channel%22%3A%22Organic%22%7D',
        'Sec-Fetch-Dest': 'document',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'www.easymarkets.com',
        'Accept-Language': 'ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
    }

    response = requests.get(
        'https://www.easymarkets.com/syc/learn-centre/discover-trading/currency-acronyms-and-abbreviations/',
        cookies=cookies,
        headers=headers,
    )
    labels_list = []
    soup = BeautifulSoup(response.text, 'html.parser')
    # soup = BeautifulSoup(response.text, 'lxml')
    # data = soup.find_all('td', class_='rtRates')
    data = soup.find_all('tr')
    for i in range(1, len(data)):
        country = data[i].td
        country = data[i].text.strip().splitlines()
        labels_list.append(country)
    return labels_list
    # return data


def fetch_exchange_rates():
    url = 'https://www.x-rates.com/table/?from=USD&amount=1'
    cookies = {
        'utag_main': 'v_id:018b01932d680014685a230138bc05075001806d00bd0$_sn:1$_ss:0$_st:1696540556740$ses_id:1696538504552%3Bexp-session$_pn:4%3Bexp-session',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        # 'Cookie': 'utag_main=v_id:018b01932d680014685a230138bc05075001806d00bd0$_sn:1$_ss:0$_st:1696540556740$ses_id:1696538504552%3Bexp-session$_pn:4%3Bexp-session',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'ru',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'www.x-rates.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Referer': 'https://www.x-rates.com/',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    params = {
        'from': 'USD',
        'amount': '1',
    }
    data_list = []
    response = requests.get('https://www.x-rates.com/table/', params=params, cookies=cookies, headers=headers)
    with open('./scripts/labels1.json', 'r') as fp:
        labels_dict = json.load(fp)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('tr')
        for i in range(12, len(data)):
            currency = data[i].text.strip().splitlines()
            if currency[0] in labels_dict:
                currency.insert(1, labels_dict[currency[0]])
            data_list.append(currency)
        currencies_df = pd.DataFrame(columns=['Full name', 'Short name', 'Curr/USD', 'USD/Curr'])
        for i in range(0, len(data_list)):
            currencies_df.loc[i] = data_list[i]
        return currencies_df
    else:
        print(f'Failed to retrieve page with status code: {response.status_code}')


def update_exchange_rates(data):
    for index, row in data.iterrows():
        currency_code = row['Short name']
        curr_to_usd = row['Curr/USD']
        currency, created = Currency.objects.get_or_create(code=currency_code)
        HistoricalExchangeRate.objects.create(
            currency=currency,
            exchange_rate=curr_to_usd,
            timestamp=timezone.now() + timedelta(hours=7)
        )

