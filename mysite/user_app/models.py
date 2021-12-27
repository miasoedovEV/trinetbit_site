from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    date_register = models.DateTimeField(verbose_name=_('дата регистрации'))
    subscription_status = models.CharField(max_length=70, verbose_name=_('статус подписки'))
    wallet_address = models.CharField(max_length=40, verbose_name=_('адрес кошелька'))
    api_key = models.CharField(default=None, max_length=18, verbose_name=_('api key'))
    api_secret = models.CharField(default=None, max_length=36, verbose_name=_('api secret'))
    bybit_user_id = models.CharField(default=None, max_length=50, verbose_name=_('id пользователя bybit'))
    email = models.EmailField(default=None, verbose_name=_('Электронная почта'))
    mailing = models.BooleanField(verbose_name=_('Рассылка'), default=None)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('index')

    class Meta:
        db_table = 'profile'
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')


class Profit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    day = models.FloatField(verbose_name=_('день'))
    month = models.FloatField(verbose_name=_('месяц'))
    year = models.FloatField(verbose_name=_('год'))
    sum_paid = models.FloatField(verbose_name=_('сумма'))

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profit'
        verbose_name = _('доходность')
        verbose_name_plural = _('доходности')


class Proxies(models.Model):
    proxy = models.CharField(max_length=100, verbose_name=_('прокси'))

    def __str__(self):
        return self.proxy

    class Meta:
        db_table = 'proxies'
        verbose_name = _('прокси')
        verbose_name_plural = _('прокси')


class TradeResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    result = models.JSONField(verbose_name=_('результаты торговли'))
    id_order_long = models.CharField(max_length=200, verbose_name=_('id ордера на лонг'), default='')
    id_order_short = models.CharField(max_length=200, verbose_name=_('id ордера на шорт'), default='')
    wallet_balance_long = models.FloatField(default=0, verbose_name=_('баланс во время открытия ордера лонг'))
    wallet_balance_short = models.FloatField(default=0, verbose_name=_('баланс во время открытия ордера шорт'))

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'trade result'
        verbose_name = _('результаты торговли')
        verbose_name_plural = _('результаты торговли')