import hashlib
import hmac
import math
from json import loads, dumps
from urllib.parse import quote_plus
from .models import Profile
import requests
import urllib3
import pandas as pd
from decimal import Decimal, getcontext

GOOD_VALUE_WALLET = 0
SYMBOL = 'USDT'
PROXY = 'http://68.183.129.76:3129'
GET_METHOD = 'GET'


def get_timestamp(proxy):
    """
    Get timestamp function
    :return: time
    """
    resp = requests.request('GET', url='https://api-testnet.bybit.com/v2/public/time', proxies={'http': proxy[0]})
    server_time = int(float(loads(resp.text)['time_now']) * 1000)
    return server_time


def go_command(method: str, url: str, secret_key: str, params: dict, proxies: dict):
    """
    Function creating a request
    :param method: GET or POST
    :type method: str
    :param url: url bybit
    :type url: str
    :param secret_key: client's secret key
    :type secret_key: str
    :param params: dict with data for request
    :type params: str
    :param proxies: dict with proxy
    :type proxies: dict
    :return: dict with data
    """

    # Create the param str
    param_str = ""
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = "true"
            else:
                v = "false"
        param_str += f"{key}={v}&"
    param_str = param_str[:-1]

    # Generate the signature
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),
                    hashlib.sha256)
    signature = hash.hexdigest()
    sign_real = {
        "sign": signature
    }
    # Prepare params in the query string format
    # quote_plus helps quote rare characters like "/" and "+"; this must be
    # applied after the signature generation.
    param_str = quote_plus(param_str, safe="=&")
    full_param_str = f"{param_str}&sign={sign_real['sign']}"
    # Request information
    if "spot" in url or method == "GET":
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = None
    else:
        headers = {"Content-Type": "application/json"}
        body = dict(params, **sign_real)

    urllib3.disable_warnings()
    s = requests.session()
    s.keep_alive = False

    # Send the request(s)

    if "spot" in url:
        # Send a request to the spot API
        response = requests.request(method, f"{url}?{full_param_str}",
                                    headers=headers, verify=False)
    else:
        # Send a request to the futures API
        if method == "POST":
            response = requests.request(method, url, data=dumps(body),
                                        headers=headers, verify=False, proxies=proxies)
        else:  # GET
            response = requests.request(method, f"{url}?{full_param_str}",
                                        headers=headers, verify=False, proxies=proxies)

    return loads(response.text)


def validate_deposit(api_key, api_secret):
    try:
        url = 'https://api.bybit.com/v2/private/wallet/balance'
        data = {"api_key": api_key, "symbol": SYMBOL, "timestamp": get_timestamp(PROXY)}
        response_balance = go_command(GET_METHOD, url, api_secret, data, {'http': PROXY})
        if response_balance['result'] is None:
            return None
        balance = float(response_balance['result'][SYMBOL]['available_balance'])
        if balance >= GOOD_VALUE_WALLET:
            return True
        else:
            return False
    except Exception:
        return None


def get_balance(user):
    profile_info = Profile.objects.get(user=user)
    try:
        url = 'https://api.bybit.com/v2/private/wallet/balance'
        data_usdt = {"api_key": profile_info.api_key, "timestamp": get_timestamp(PROXY)}
        response_balance = go_command(GET_METHOD, url, profile_info.api_secret, data_usdt, {'http': PROXY})
        if response_balance['result'] is None:
            return None, None
        balance_usdt = round(float(response_balance['result'][SYMBOL]['available_balance']), 2)
        balance_btc = round(float(response_balance['result']["BTC"]['available_balance']), 2)
        return balance_btc, balance_usdt
    except Exception:
        return None, None


def get_user_id(api_key, api_secret):
    url = 'https://api.bybit.com/v2/private/account/api-key'
    data = {"api_key": api_key, "timestamp": get_timestamp(PROXY)}
    response = go_command(GET_METHOD, url, api_secret, data, {'http': PROXY})
    user_id = response['result'][0]['user_id']
    return user_id


def find_price(symbol):
    try:
        url = 'https://api.bybit.com/v2/public/tickers'
        response_currency = requests.request('GET', url, verify=False, proxies={'http': PROXY})
        response_currency = loads(response_currency.text)
        for dict_info in response_currency['result']:
            if dict_info['symbol'] == symbol:
                last_price = dict_info['last_price']
                return last_price
    except Exception:
        pass


def usdt_to_btc(usdt: float, currency: float):
    """
    Transfer usdt to btc
    :param usdt: usdt value
    :type usdt: float
    :param currency: currency
    :type currency: float
    :return: btc value
    :rtype: float
    """
    btc = usdt / float(currency)
    return btc


def my_round(value, step):
    """
    Funсtion round value
    :param value: value
    :type value: float
    :return: value
    :rtype: float
    """
    dif = value * 10 ** step
    dif = math.floor(dif)
    true_value = dif / (10 ** step)
    return true_value


def get_result_trade(user):
    getcontext().prec = 3
    profile_info = Profile.objects.get(user=user)
    url_get_fund_records = 'https://api.bybit.com//v2/private/wallet/fund/records'
    data = {"api_key": profile_info.api_key, "coin": 'USDT', "timestamp": get_timestamp(PROXY), "page": 1,
            "wallet_fund_type": "RealisedPNL", "limit": 50}
    response = go_command(GET_METHOD, url_get_fund_records, profile_info.api_secret, data, {'http': PROXY})
    if response['result']['data'] is None:
        return None
    df = pd.DataFrame(response['result']['data'])
    list_data = []
    last_price = find_price('BTCUSDT')
    for index, time in enumerate(df.exec_time.values):
        balance_changes = Decimal(df.amount.values[index]) * 100 / Decimal(df.wallet_balance.values[index])
        changes_in_btc = Decimal(usdt_to_btc(float(df.amount.values[index]), last_price))
        changes_in_usdt = Decimal(df.amount.values[index])
        if changes_in_usdt > 0:
            balance_direction = 'up'
        else:
            balance_direction = 'down'
        if index != 0:
            if df.exec_time.values[index][8:10] == df.exec_time.values[index - 1][8:10]:
                list_data[-1][1] += balance_changes
                list_data[-1][2] += changes_in_btc
                list_data[-1][3] += changes_in_usdt
                if list_data[-1][3] > 0:
                    balance_direction = 'up'
                else:
                    balance_direction = 'down'
                list_data[-1][5] = balance_direction
            else:
                list_data.append([f"#{df.id.values[index]}", balance_changes, changes_in_btc, changes_in_usdt,
                                  df.exec_time.values[index][0:10], balance_direction])
        else:
            list_data.append([f"#{df.id.values[index]}", balance_changes, changes_in_btc, changes_in_usdt,
                              df.exec_time.values[index][0:10], balance_direction])
    return list_data
