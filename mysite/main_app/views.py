from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def about_project_view(request):
    try:
        return render(request, 'about_project.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def faq_view(request):
    try:
        return render(request, 'faq.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def index_view(request):
    try:
        return render(request, 'index.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def view_404(request):
    try:
        return render(request, '404.html', {'title': 'error'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def view_private_policity(request):
    try:
        return render(request, 'private_policity.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def view_eula(request):
    try:
        return render(request, 'eula.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))


def view_guide(request):
    try:
        return render(request, 'guide.html', {'title': 'Trinetbit'})
    except Exception:
        HttpResponseRedirect(reverse('error'))

# Create your views here.
