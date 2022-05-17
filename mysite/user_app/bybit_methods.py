import hashlib
import hmac
import math
from json import loads, dumps
from urllib.parse import quote_plus
from .models import Profile, Proxies, TradeResult
import requests
import urllib3

GOOD_VALUE_WALLET = 200
SYMBOL = 'USDT'
GET_METHOD = 'GET'


def get_proxy():
    proxy = Proxies.objects.order_by('?').first()
    dict_proxy = {'http': f'http://{proxy}'}
    return dict_proxy


def get_timestamp(proxy):
    """
    Get timestamp function
    :return: time
    """
    resp = requests.request('GET', url='https://api.bybit.com/v2/public/time', proxies=proxy)
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
    proxy = get_proxy()
    try:
        url = 'https://api.bybit.com/v2/private/wallet/balance'
        data = {"api_key": api_key, "symbol": SYMBOL, "timestamp": get_timestamp({'http': proxy})}
        response_balance = go_command(GET_METHOD, url, api_secret, data, {'http': proxy})
        if response_balance['result'] is None:
            return None
        balance = float(response_balance['result'][SYMBOL]['available_balance'])
        if balance >= GOOD_VALUE_WALLET:
            return True
        else:
            return False
    except Exception:
        return None


def get_balance(user=None, api_key=None, api_secret=None):
    if user is not None:
        profile_info = Profile.objects.get(user=user)
        api_key = profile_info.api_key
        api_secret = profile_info.api_secret
    proxy = get_proxy()
    try:
        url = 'https://api.bybit.com/v2/private/wallet/balance'
        data_usdt = {"api_key": api_key, "timestamp": get_timestamp(proxy)}
        response_balance = go_command(GET_METHOD, url, api_secret, data_usdt, proxy)
        if response_balance['result'] is None:
            return None, None
        balance_usdt = round(float(response_balance['result'][SYMBOL]['available_balance']), 2)
        balance_btc = round(float(response_balance['result']["BTC"]['available_balance']), 2)
        return balance_btc, balance_usdt
    except Exception:
        return None, None


def get_user_id(api_key, api_secret):
    proxy = get_proxy()
    url = 'https://api.bybit.com/v2/private/account/api-key'
    data = {"api_key": api_key, "timestamp": get_timestamp(proxy)}
    response = go_command(GET_METHOD, url, api_secret, data, proxy)
    user_id = response['result'][0]['user_id']
    return user_id


def find_price(symbol):
    try:
        proxy = get_proxy()
        url = 'https://api.bybit.com/v2/public/tickers'
        response_currency = requests.request('GET', url, verify=False, proxies=proxy)
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
    profit_info = TradeResult.objects.get(user=user)
    info_trade = loads(profit_info.result)
    trade_result = info_trade['info_trade']
    trade_result.reverse()
    list_data = []
    for index, dict_info in enumerate(trade_result):
        if dict_info['balance_change_usdt'] > 0:
            balance_direction = 'up'
        else:
            balance_direction = 'down'
        list_data.append([f"#{index + 1}", dict_info['balance_change_percent'], dict_info['balance_change_btc'],
                          dict_info['balance_change_usdt'], dict_info['date'], balance_direction])
        if len(list_data) == 10:
            break
    return list_data
