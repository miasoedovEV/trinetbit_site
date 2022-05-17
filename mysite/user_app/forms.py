from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from validate_email import validate_email
from .bybit_methods import validate_deposit
from django.utils.translation import gettext_lazy as _

SETTINGS_REGISTER_INPUT = {
    "api_key": dict(name_class='register-input', id='key', placeholder=_('API Ключ')),
    "api_secret": dict(name_class='register-input', id='api', placeholder=_('API Секрет')),
    "username": dict(name_class='register-input', id='userName', placeholder=_('Имя пользователя')),
    "email": dict(name_class='register-input', id='email', placeholder='Email'),
    "wallet_address": dict(name_class='register-input', id='wallet', placeholder=_('BTC Кошелёк')),
    "password1": dict(name_class='register-input', id='password', placeholder=_('Пароль')),
    "password2": dict(name_class='register-input', id='repeatPassword', placeholder=_('Повторите пароль')),
    "agreement": dict(name_class='form-check-input', id='flexCheckDefault'),
    "mailing": dict(name_class='form-check-input', id='flexCheckChecked'),

}


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, min_length=3)
    wallet_address = forms.CharField()
    password1 = forms.CharField(min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=5, widget=forms.PasswordInput)
    api_key = forms.CharField(max_length=18, min_length=18)
    api_secret = forms.CharField(max_length=36, min_length=36)
    email = forms.EmailField()
    agreement = forms.BooleanField()
    mailing = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = SETTINGS_REGISTER_INPUT[name]['name_class']
            field.widget.attrs['id'] = SETTINGS_REGISTER_INPUT[name]['id']
            if name != 'agreement' and name != 'mailing':
                field.widget.attrs['placeholder'] = SETTINGS_REGISTER_INPUT[name]['placeholder']

    def clean(self):
        cleaned_data = super().clean()
        api_key = cleaned_data.get("api_key")
        api_secret = cleaned_data.get("api_secret")
        email = cleaned_data.get("email")
        result_validate_balance = validate_deposit(api_key, api_secret)
        agreement = cleaned_data.get('agreement')
        if result_validate_balance is False:
            msg = _("Недостаточно баланса!")
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
        elif result_validate_balance is None:
            msg = _("Неверные api key и api secret!")
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
        try:
            answer_email = validate_email(email)
        except Exception:
            answer_email = False
        if answer_email is False:
            msg = _("Неверный формат почты!")
            self.add_error('email', msg)
        if agreement is False:
            msg = _("Вы не подтвердили пользовательское соглашение!")
            self.add_error('agreement', msg)

    class Meta:
        model = User
        fields = ('username', 'wallet_address', 'password1', 'password2', 'api_key', 'api_secret', 'email')


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label="Code", required=False)
    user_code = None

    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = "login-input w-100"
        self.fields['code'].widget.attrs['placeholder'] = _("Код")

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        if code != self.user_code:
            msg = _("Неверный код!")
            self.add_error('code', msg)


class PasswordForm(forms.Form):
    old_password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    password1 = forms.CharField(min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=5, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "old_password":
                field.widget.attrs['class'] = "w-50 modal-input"
                field.widget.attrs['placeholder'] = _("Введите старый пароль")
            elif name == "password1":
                field.widget.attrs['class'] = "w-50 modal-input mt-5 mb-3"
                field.widget.attrs['placeholder'] = _("Введите новый пароль")
            else:
                field.widget.attrs['class'] = "w-50 modal-input"
                field.widget.attrs['placeholder'] = _("Повторите пароль")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password2 != password1:
            msg = "Password mismatch!"
            self.add_error('password1', msg)
            self.add_error('password2', msg)


class WalletForm(forms.Form):
    wallet_address = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        self.fields['wallet_address'].widget.attrs['class'] = "w-100 modal-input"
        self.fields['wallet_address'].widget.attrs['placeholder'] = _("Введите новый кошелёк")


class ApiForm(forms.Form):
    api_key = forms.CharField(max_length=18, min_length=18)
    api_secret = forms.CharField(max_length=36, min_length=36)

    def __init__(self, *args, **kwargs):
        super(ApiForm, self).__init__(*args, **kwargs)
        self.fields['api_key'].widget.attrs['class'] = "w-100 modal-input"
        self.fields['api_key'].widget.attrs['placeholder'] = _("Введите новый ключ")
        self.fields['api_secret'].widget.attrs['class'] = "w-100 modal-input mt-3"
        self.fields['api_secret'].widget.attrs['placeholder'] = _("Введите новый секрет")

    def clean(self):
        cleaned_data = super().clean()
        api_key = cleaned_data.get("api_key")
        api_secret = cleaned_data.get("api_secret")
        result_validate_balance = validate_deposit(api_key, api_secret)
        if result_validate_balance is False:
            msg = _("Недостаточно баланса!")
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
        elif result_validate_balance is None:
            msg = _("Неверные api key и api secret!")
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
