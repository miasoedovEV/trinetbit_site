from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, UpdateView
from .models import Profit
from .forms import RegisterForm, VerificationForm, PasswordForm, WalletForm, ApiForm
from datetime import datetime
from .bybit_methods import *
from django.core.cache import cache
from json import dumps, loads
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

RANDOM_VALUES_HUGE = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                      'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                      'Z', 'X', 'C', 'V', 'B', 'N', 'M']

DICT_ADDRESS = {'mail.ru': ['stincs01@mail.ru', 'gogius369'],
                'gmail.com': ['stincs01@gmail.com', 'CERFujyljy369']}

RANDOM_VALUES_LOW = [value.lower() for value in RANDOM_VALUES_HUGE]

# create message object instance
MSG = MIMEMultipart()
MESSAGE = "Good day!"
# setup the parameters of the message
verification_code_subject = "Code for verification from TRINETBIT"
new_password_subject = "New password for TRINETBIT"


def send_mail(type_email, email, message, subject):
    # add in the message body
    MSG['From'] = DICT_ADDRESS[type_email][0]
    password = DICT_ADDRESS[type_email][1]
    MSG.attach(MIMEText(MESSAGE, 'plain'))
    # create server
    server = smtplib.SMTP(f'smtp.{type_email}: 587')
    server.starttls()
    server.login(MSG['From'], password)
    MSG['Subject'] = subject
    BODY = "\r\n".join((
        "From: %s" % MSG['From'],
        "To: %s" % email,
        "Subject: %s" % MSG['Subject'],
        "",
        message
    ))
    # send the message via the server.
    server.sendmail(MSG['From'], email, BODY)
    server.quit()


def generate_code():
    code = ''
    index_list = random.randint(1, 2)
    if index_list == 1:
        list_1 = RANDOM_VALUES_HUGE
        list_2 = RANDOM_VALUES_LOW
    else:
        list_2 = RANDOM_VALUES_HUGE
        list_1 = RANDOM_VALUES_LOW
    for _ in range(2):
        code += random.choice(list_1)
    for _ in range(2):
        code += random.choice(list_2)
    for _ in range(2):
        code += str(random.randint(0, 9))
    return code


def generate_password():
    password = ''
    index_list = random.randint(1, 2)
    if index_list == 1:
        list_1 = RANDOM_VALUES_HUGE
        list_2 = RANDOM_VALUES_LOW
    else:
        list_2 = RANDOM_VALUES_HUGE
        list_1 = RANDOM_VALUES_LOW
    for _ in range(2):
        password += random.choice(list_1)
    for _ in range(2):
        password += random.choice(list_2)
    for _ in range(4):
        password += str(random.randint(0, 9))
    return password


class MyLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(MyLoginView, self).get_context_data()
        context['title'] = 'Login'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('reautification') is not None:
            username = request.POST.get('username')
            if request.POST.get('username') is not None:
                username = username
                try:
                    user = User.objects.get(username__exact=username)
                except Exception:
                    user = None
                if user is not None:
                    profile = Profile.objects.get(user=user)
                    email = profile.email
                    type_email = email.split('@')[1]
                    password = generate_password()
                    user.set_password(password)
                    user.save()
                    send_mail(type_email, email, generate_password(), new_password_subject)
        return super(MyLoginView, self).post(request)


class MyLogoutView(LogoutView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data()
        context['title'] = 'Register'
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data.get('api_key')
            api_secret = form.cleaned_data.get('api_secret')
            username = form.cleaned_data.get('username')
            wallet_address = form.cleaned_data.get('wallet_address')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            agreement = form.cleaned_data.get('agreement')
            mailing = form.cleaned_data.get('mailing')
            data_info = dict(username=username, password1=password, password2=password, api_key=api_key,
                             api_secret=api_secret,
                             wallet_address=wallet_address,
                             email=email,
                             agreement=agreement,
                             mailing=mailing)
            cache.set('data_info', dumps(data_info))
            code = generate_code()
            cache.set('code', code)
            type_email = email.split('@')[1]
            send_mail(type_email, email, code, verification_code_subject)
            return HttpResponseRedirect(reverse('verification'))
        messages = [mes for mes in dict(form.errors).values()]
        return render(request, self.template_name, {'form': form, 'title': 'Register', 'error_message': messages[0]})


# Create your views here.

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile.html'
    fields = ['wallet_address', 'api_key', 'api_secret']

    def get_object(self, queryset=None):
        self.kwargs['pk'] = self.request.user.profile.id
        return super(ProfileView, self).get_object()

    def create_context(self, context):
        context['title'] = 'Personal account'
        context['list_data'] = get_result_trade(self.request.user)
        context["balance_btc"], context["balance_usdt"] = get_balance(self.request.user)
        profit = Profit.objects.get(user=self.request.user)
        context["day_profit"] = profit.day
        context["month_profit"] = profit.month
        context["year_profit"] = profit.year
        context["sum_paid"] = profit.sum_paid
        profile = Profile.objects.get(user=self.request.user)
        if profile.subscription_status != 'Active':
            message = profile.subscription_status
            message_list = message.split(';')
            context["status"] = message_list[0]
            context["cause"] = message_list[1]
            context['status_code'] = '1'
        else:
            context["status"] = profile.subscription_status
            context['status_code'] = '0'
        wallet_address = profile.wallet_address
        context["wallet"] = wallet_address[0:3] + '...' + wallet_address[-3::]
        context["id_wallet"] = wallet_address
        context["form_pass"] = PasswordForm()
        context["form_wall"] = WalletForm()
        context["form_api"] = ApiForm()
        context["password"] = '*' * 9
        context['result'] = 'none'
        context['message'] = 'Data updated successfully!'
        context['api_key'] = profile.api_key
        context['api_secret'] = profile.api_secret
        return context

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        return self.create_context(context)

    def post(self, request, *args, **kwargs):
        context = self.create_context(context={})
        old_password = request.POST.get('old_password')
        if request.POST.get('wallet_address') is not None:
            form = WalletForm(request.POST)
        elif old_password is not None:
            if request.user.check_password(old_password):
                form = PasswordForm(request.POST)
            else:
                context['result'] = 'error'
                context['message'] = 'Invalid old password!'
                return render(request, self.template_name, context)
        else:
            form = ApiForm(request.POST)
        if form.is_valid():
            if old_password is not None:
                user = User.objects.get(username__exact=request.user.username)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)
                context['result'] = 'good'
                context['message'] = 'Data updated successfully!'
                return render(request, self.template_name, context)
            profile = Profile.objects.get(user=request.user)
            if request.POST.get('wallet_address') is not None:
                profile.wallet_address = form.cleaned_data['wallet_address']
            else:
                profile.api_key = form.cleaned_data['api_key']
                profile.api_secret = form.cleaned_data['api_secret']
            profile.save()
            context['result'] = 'good'
            context['message'] = 'Data updated successfully!'
            return render(request, self.template_name, context)
        context['result'] = 'error'
        messages = [mes for mes in dict(form.errors).values()]
        context['message'] = messages[0] + '!'
        return render(request, self.template_name, context)


class VerificationView(FormView):
    template_name = 'verification.html'
    form_class = VerificationForm

    def get_context_data(self, **kwargs):
        context = super(VerificationView, self).get_context_data()
        context['title'] = 'Verification'
        return context

    def post(self, request, *args, **kwargs):
        form = VerificationForm(request.POST)
        try:
            data_info = loads(cache.get('data_info'))
        except Exception:
            return HttpResponseRedirect(reverse('register'))
        code = cache.get('code')
        form.user_code = code
        if form.is_valid():
            form_register = RegisterForm(data_info)
            form_register.is_valid()
            user = form_register.save()
            api_key = form_register.cleaned_data.get('api_key')
            api_secret = form_register.cleaned_data.get('api_secret')
            username = form_register.cleaned_data.get('username')
            wallet_address = form_register.cleaned_data.get('wallet_address')
            date_register = datetime.now()
            bybit_user_id = get_user_id(api_key, api_secret)
            subscription_status = 'Active'
            email = form_register.cleaned_data.get('email')
            mailing = form_register.cleaned_data.get('mailing')
            Profile.objects.create(
                user=user,
                api_key=api_key,
                api_secret=api_secret,
                date_register=date_register,
                bybit_user_id=bybit_user_id,
                subscription_status=subscription_status,
                wallet_address=wallet_address,
                email=email,
                mailing=mailing
            )
            Profit.objects.create(
                user=user,
                day=0.0,
                month=0.0,
                year=0.0,
                sum_paid=0.0
            )
            raw_password = form_register.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            cache.delete('data_info')
            cache.delete('code')
            return HttpResponseRedirect(reverse('index'))
        cache.set('data_info', dumps(data_info))
        if 'resending' in request.POST.keys():
            code = generate_code()
            cache.set('code', code)
            type_email = data_info['email'].split('@')[1]
            send_mail(type_email, data_info['email'], code, verification_code_subject)
            return HttpResponseRedirect(reverse('verification'))
        cache.set('code', code)
        return render(request, self.template_name, {'form': form, 'title': 'Verification'})

# Create your views here.
