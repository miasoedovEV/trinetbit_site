from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_register = models.DateTimeField(verbose_name='дата регистрации')
    subscription_status = models.CharField(max_length=70, verbose_name='статус подписки')
    wallet_address = models.CharField(max_length=40, verbose_name='адрес кошелька')
    api_key = models.CharField(default=None, max_length=18, verbose_name='api key')
    api_secret = models.CharField(default=None, max_length=36, verbose_name='api secret')
    bybit_user_id = models.CharField(default=None, max_length=50, verbose_name='id пользователя bybit')
    email = models.EmailField(default=None, verbose_name='Электронная почта')
    mailing = models.BooleanField(verbose_name='Рассылка', default=None)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('index')

    class Meta:
        db_table = 'profile'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Profit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    day = models.FloatField(verbose_name='день')
    month = models.FloatField(verbose_name='месяц')
    year = models.FloatField(verbose_name='год')
    sum_paid = models.FloatField(verbose_name='сумма')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profit'
        verbose_name = 'доходность'
        verbose_name_plural = 'доходности'


class Proxies(models.Model):
    proxy = models.CharField(max_length=100, verbose_name='прокси')

    def __str__(self):
        return self.proxy

    class Meta:
        db_table = 'proxies'
        verbose_name = 'прокси'
        verbose_name_plural = 'прокси'


class TradeResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    result = models.JSONField(verbose_name='результаты торговли')
    wallet_balance_morning = models.FloatField(default=0, verbose_name="баланс утром")

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'traderesult'
        verbose_name = 'результаты торговли'
        verbose_name_plural = 'результаты торговли'


class SupportCheckPaid(models.Model):
    calculated_per_day = models.JSONField(verbose_name='проверенные транзакции')

    class Meta:
        db_table = 'supportcheckpaid'
        verbose_name = 'проверка оплаты'
        verbose_name_plural = 'проверка оплаты'
