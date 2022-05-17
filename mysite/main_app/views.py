from django.shortcuts import render
from django.template import RequestContext
from django.template.context_processors import csrf
from user_app.models import Profile, Profit

ADD_CLIENTS = 117
BALANCE_ADD_CLIENTS = 1000
PROFIT_PERCENT = 12.5


def about_project_view(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    return render(request, 'about_project.html', context)


def faq_view(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    return render(request, 'faq.html', context)


def index_view(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    amount_users = Profile.objects.count()
    context['amount_users'] = amount_users + ADD_CLIENTS
    if context['amount_users'] == ADD_CLIENTS:
        context['total_profit'] = int(BALANCE_ADD_CLIENTS * PROFIT_PERCENT / 100 * 117)
    else:
        profit_users = sum([profit.month for profit in Profit.objects.all()])
        context['total_profit'] = int(BALANCE_ADD_CLIENTS * PROFIT_PERCENT / 100 * 117) + profit_users
    context['average_customer_profit'] = int(context['total_profit'] / context['amount_users'])
    return render(request, 'index.html', context)


def view_404(request, exception):
    context = RequestContext(request)
    context['title'] = 'error'
    response = render(request, '404.html', context)
    response.status_code = 404
    return response


def view_500(request):
    context = RequestContext(request)
    context['title'] = 'error'
    response = render(request, '500.html', context)
    response.status_code = 500
    return response


def csrf_failure(request, reason=""):
    context = RequestContext(request)
    context['title'] = 'error'
    response = render(request, '403.html', context)
    response.status_code = 403
    return response


def view_private_policity(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    return render(request, 'private_policity.html', context)


def view_eula(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    return render(request, 'eula.html', context)


def view_guide(request):
    context = dict()
    context['title'] = 'Trinetbit'
    context.update(csrf(request))
    return render(request, 'guide.html', context)

# Create your views here.
