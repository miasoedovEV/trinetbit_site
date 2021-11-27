from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from validate_email import validate_email
from .bybit_methods import validate_deposit


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
            if name == 'agreement' or name == 'mailing':
                field.widget.attrs['class'] = "check_input"
            elif name == 'password1':
                field.widget.attrs['class'] = "label label-pass-img-left"
            elif name == 'password2':
                field.widget.attrs['class'] = "label label-pass-img"
            else:
                field.widget.attrs['class'] = "label"

    def clean(self):
        cleaned_data = super().clean()
        api_key = cleaned_data.get("api_key")
        api_secret = cleaned_data.get("api_secret")
        email = cleaned_data.get("email")
        result_validate_balance = validate_deposit(api_key, api_secret)
        agreement = cleaned_data.get('agreement')
        if result_validate_balance is False:
            msg = "Not enough balance!"
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
        elif result_validate_balance is None:
            msg = "Invalid api key and api secret!"
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
        try:
            answer_email = validate_email(email)
        except Exception:
            answer_email = False
        if answer_email is False:
            msg = "Email format is incorrect!"
            self.add_error('email', msg)
        if agreement is False:
            msg = "You have not confirmed the user agreement with an agreement!"
            self.add_error('agreement', msg)

    class Meta:
        model = User
        fields = ('username', 'wallet_address', 'password1', 'password2', 'api_key', 'api_secret', 'email')


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label=_('Код'), required=False)
    user_code = None

    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = "label"

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        if code != self.user_code:
            msg = "Error code!"
            self.add_error('code', msg)


class PasswordForm(forms.Form):
    old_password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    password1 = forms.CharField(min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=5, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "change-pass update-input pass-edit"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password2 != password1:
            msg = "Password mismatch!"
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)


class WalletForm(forms.Form):
    wallet_address = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        self.fields['wallet_address'].widget.attrs['class'] = "update-input"


class ApiForm(forms.Form):
    api_key = forms.CharField(max_length=18, min_length=18)
    api_secret = forms.CharField(max_length=36, min_length=36)

    def __init__(self, *args, **kwargs):
        super(ApiForm, self).__init__(*args, **kwargs)
        self.fields['api_key'].widget.attrs['class'] = "update-input change-pass"
        self.fields['api_secret'].widget.attrs['class'] = "update-input change-pass"

    def clean(self):
        cleaned_data = super().clean()
        api_key = cleaned_data.get("api_key")
        api_secret = cleaned_data.get("api_secret")
        result_validate_balance = validate_deposit(api_key, api_secret)
        if result_validate_balance is False:
            msg = "Not enough balance!"
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
        elif result_validate_balance is None:
            msg = "Invalid api key and api secret!"
            self.add_error('api_key', msg)
            self.add_error('api_secret', msg)
            return
